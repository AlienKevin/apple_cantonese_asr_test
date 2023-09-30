# Evaluation of Apple's Cantonese speech recognition on Common Voice

I'm interested in developing a speech-powered Cantonese learning app for iOS but can't find qualitative evaluations of Apple's ASR model.
Hence, I conducted an evaluation on two versions of the Common Voice Yue dataset and one version of the Common Voice zh-HK dataset. Note that the Yue dataset contains purely colloquial Cantonese while the older zh-HK dataset contains a mixture of colloquial and formal language usages.

* **Common Voice 11 Yue**: Contains 2438 test audios.
    - Currenet state-of-the-art [simonl0909/whisper-large-v2-cantonese](https://huggingface.co/simonl0909/whisper-large-v2-cantonese) achieves a **6.727% CER**. However, Simon's model was trained on the Common Voice dataset so it might not be a fair comparison. The Common Voice dataset may be different from training data used for the Apple model, which can increase the recognition difficulty.
* **Common Voice 15 Yue**: The latest version of the dataset as of Sep 27, 2023. Contains 2560 test audios.
* **Common Voice 11 zh-HK**: Commonly used by open source ASR models for training and evaluation. Contains 5591 test audios.
    - Current [state-of-the-art developed by HKUST](https://arxiv.org/pdf/2201.02419.pdf) achieves a **7.65% CER**. However, HKUST's model was also trained on the Common Voice dataset along with their MDCC dataset so it might not be a fair comparison.

Two kinds of Character Error Rates are computed:
1. CER on the top prediction outputted by Apple's ASR
2. The minimum CER on all prediction candidates outputted by Apple's ASR. Or in other words, I pick the prediction candidate that has the closest levenshtein distance to the reference sentence and calculate its CER.

## macOS Ventura vs Sonoma

![CER Comparison Chart](media/cer_comparison.png)

Here are the numbers obtained using macOS Ventura 13.6 (22G120) on a M1 Max macBook Pro:
| Dataset               | Top Predictions CER Score  | Closest Predictions CER Score |
|-----------------------|-----------------------------|-------------------------------|
| Common Voice 15 yue   | 10.525%                     | 5.999%                        |
| Common Voice 11 yue   | 10.335%                     | 5.886%                        |
| Common Voice 11 zh-HK | 9.831%                      | 7.028%                        |
| Guangzhou Daily Use   | 8.681%                      | 6.348%                        |

And here are the numbers obtained using macOS Sonoma 14.0 (23A344) on the same M1 Max macBook Pro:
| Dataset               | Top Predictions CER Score  | Closest Predictions CER Score |
|-----------------------|-----------------------------|-------------------------------|
| Common Voice 15 yue   | 7.417%                      | 5.869%                        |
| Common Voice 11 yue   | 7.381%                      | 5.819%                        |
| Common Voice 11 zh-HK | 8.114%                      | 6.625%                        |
| Guangzhou Daily Use   | 7.409%                      | 5.160%                        |

## macOS Sonoma vs Cloud APIs

For comparison, here are the results of macOS Sonoma speech API, Google Speech-to-text v1p1beta1, and Microsoft Cognitive Services Speech-to-text on the Common Voice 15 yue dataset:

![Competitor CER Comparison Chart](media/competitor_cer_comparison.png)

| Dataset               | Top Predictions CER Score  | Closest Predictions CER Score |
|-----------------------|-----------------------------|-------------------------------|
| macOS Sonoma          | 7.417%                      | 5.869%                        |
| Google                | 11.392%                     | 5.718%                        |
| Microsoft             | 22.549%                     | 8.960%                        |

# Dataset statistics

## Audio durations

![CV 15 Yue Audio Durations Chart](media/cv_15_yue_audio_durations.png)

![CV 11 Yue Audio Durations Chart](media/cv_11_yue_audio_durations.png)

![CV 11 zh-hk Audio Durations Chart](media/cv_11_zh_hk_audio_durations.png)

![Guangzhou Daily Use Audio Durations Chart](media/guangzhou_daily_use_audio_durations.png)


# Minor Preprocessing
For the zh-HK test set, we changed the ASCII double quotes to Chinese-style double quotes because of TSV parsing issues:
```
common_voice_zh-HK_23107405.mp3   同事找來一對桌上"小"揚聲器 => 同事找來一對桌上“小”揚聲器
```

When calculating the WER, we always strip away the punctuations first.
The Guangzhou Daily Use corpus uses uncommon character variants of two Cantonese particles so we replace all such characters
with their canonical forms.
```
噶 => 㗎
咧 => 呢
```
