import Speech
import SwiftCSV
import Tqdm

@available(macOS 10.15, *)
func recognizeFile(url: URL) async throws -> [Segment] {
  guard let myRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "yue-CN")) else {
    throw NSError(
      domain: "RecognitionError", code: 1,
      userInfo: ["message": "The system doesn't support the zh-HK locale."])
  }

  myRecognizer.supportsOnDeviceRecognition = true

  guard myRecognizer.isAvailable else {
    throw NSError(
      domain: "RecognitionError", code: 2, userInfo: ["message": "The recognizer isn't available."])
  }

  let request = SFSpeechURLRecognitionRequest(url: url)
  request.shouldReportPartialResults = true
  request.taskHint = .dictation

  return try await withCheckedThrowingContinuation { continuation in
    myRecognizer.recognitionTask(with: request) { (result, error) in
      if let error = error {
        continuation.resume(throwing: error)
        return
      }

      if let result = result, result.isFinal {
        continuation.resume(
          returning: result.bestTranscription.segments.map({ Segment(segment: $0) }))
      }
    }
  }
}

struct RecognitionResult: Codable {
  var path: String
  var sentence: String
  var segments: [Segment]
}

struct Segment: Codable {
  var substring: String
  var alternativeSubstrings: [String]
  var confidence: Float
  var timestamp: TimeInterval
  var duration: TimeInterval

  @available(macOS 10.15, *)
  init(segment: SFTranscriptionSegment) {
    substring = segment.substring
    alternativeSubstrings = segment.alternativeSubstrings
    confidence = segment.confidence
    timestamp = segment.timestamp
    duration = segment.duration
  }
}

@available(macOS 10.15, *)
func runSpeechRecognition(datasetName: String = "common-voice-15") async throws {
  let metadata: CSV = try CSV<Named>(
    url: URL(fileURLWithPath: "data/\(datasetName)/test.tsv"), delimiter: .tab)

  var results: [RecognitionResult] = []
  for row in TqdmSequence(sequence: metadata.rows) {
    if let path = row["path"], let sentence = row["sentence"] {
      // print("Processing \(path)")
      let url = URL(fileURLWithPath: "data/\(datasetName)/test/\(path)")
      do {
        let segments = try await recognizeFile(url: url)
        let result = RecognitionResult(
          path: path,
          sentence: sentence,
          segments: segments
        )
        results.append(result)
      } catch {
        print("Error: " + error.localizedDescription)
      }
    }
  }

  let encoder = JSONEncoder()
  let currentWorkingPath = FileManager.default.currentDirectoryPath
  let transcriptionsFile = URL(fileURLWithPath: currentWorkingPath).appendingPathComponent(
    "\(datasetName)-transcriptions.json")
  let jsonData = try encoder.encode(results)
  if let jsonString = String(data: jsonData, encoding: .utf8) {
    try jsonString.write(to: transcriptionsFile, atomically: true, encoding: .utf8)
  }
}

@available(macOS 14, *)
func generateCustomLM(datasetName: String) async throws {
  let data = SFCustomLanguageModelData(
    locale: Locale(identifier: "zh_HK"),
    identifier: "com.kevin.\(datasetName)", version: "1.0")

  let vocab: CSV = try CSV<Named>(
    url: URL(fileURLWithPath: "vocab/\(datasetName).tsv"), delimiter: .tab)

  for row in TqdmSequence(sequence: vocab.rows) {
    guard let word = row["word"] else {
      print("Error: word is nil")
      continue
    }
    guard let count = row["count"] else {
      print("Error: count is nil")
      continue
    }
    // increase frequency of each word
    guard let count = Int(count) else {
      print("Error: count is not an integer")
      continue
    }
    data.insert(
      // increase frequency of each word
      phraseCount: SFCustomLanguageModelData.PhraseCount.init(phrase: word, count: count * 10))
  }

  let url = URL(filePath: FileManager.default.currentDirectoryPath + "/customLM/\(datasetName).bin")
  try await data.export(to: url)

  print("Finished exporting custom language model to \(url)")
}

if #available(macOS 14, *) {
  try await generateCustomLM(datasetName: "common-voice-15")
} else {
  print("macOS version must be above or equal to 10.15")
}
