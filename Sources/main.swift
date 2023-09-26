import Speech

@available(macOS 10.15, *)
func recognizeFile(url: URL) async throws -> [String] {
    guard let myRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "zh-HK")) else {
        throw NSError(domain: "RecognitionError", code: 1, userInfo: ["message": "The system doesn't support the zh-HK locale."])
    }
    
    guard myRecognizer.isAvailable else {
        throw NSError(domain: "RecognitionError", code: 2, userInfo: ["message": "The recognizer isn't available."])
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
                continuation.resume(returning: result.transcriptions.map { $0.formattedString })
            }
        }
    }
}

let url = URL(fileURLWithPath: "data/common-voice-11/test/common_voice_yue_32267927.mp3")

if #available(macOS 10.15, *) {
    do {
        let transcription = try await recognizeFile(url: url)
        print("Transcriptions: \(transcription)")
    } catch {
        print("Speech recognition failed: \(error)")
    }
} else {
    print("Speech recognition is not supported.")
}
