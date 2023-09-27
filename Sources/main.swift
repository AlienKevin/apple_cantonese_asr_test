import Speech
import SwiftCSV

@available(macOS 10.15, *)
func recognizeFile(url: URL) async throws -> [Segment] {
  guard let myRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "zh-HK")) else {
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

if #available(macOS 10.15, *) {
  let metadata: CSV = try CSV<Named>(
    url: URL(fileURLWithPath: "data/common-voice-11/test.tsv"), delimiter: .tab)

  var results: [RecognitionResult] = []
  for row in metadata.rows {
    if let path = row["path"], let sentence = row["sentence"] {
      print("Processing \(path)")
      let url = URL(fileURLWithPath: "data/common-voice-11/test/\(path)")
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
    "common-voice-11-transcriptions.json")
  let jsonData = try encoder.encode(results)
  if let jsonString = String(data: jsonData, encoding: .utf8) {
    try jsonString.write(to: transcriptionsFile, atomically: true, encoding: .utf8)
  }
} else {
  print("Speech recognition is not supported.")
}
