# Evaluation of Apple's Cantonese speech recognition on Common Voice

I'm interested in developing a speech-powered Cantonese learning app for iOS but can't find qualitative evaluations of Apple's ASR model.
Hence, I conducted an evaluation on two versions of the public Common Voice Yue dataset. Note that the Yue dataset contains purely colloquial Cantonese while the older zh-HK dataset contains a mixture of colloquial and formal language usages. Since I'm more interested in colloquial usages, I will be evaluating the model on the Yue dataset.

* **Common Voice 11**: Commonly used by open source ASR models for training and evaluation. Contains 2438 test audios.
    - Currenet state-of-the-art open source Cantonese ASR [simonl0909/whisper-large-v2-cantonese](https://huggingface.co/simonl0909/whisper-large-v2-cantonese) achieves a **6.727% CER**. However, Simon's model was trained on the Common Voice dataset so it's not a direct apples-to-apples comparison. The Common Voice dataset may be out-of-domain data for the Apple model, which can increase the recognition difficulty significantly (see https://arxiv.org/pdf/2201.02419.pdf).
* **Common Voice 15**: The latest version of the dataset as of Sep 27, 2023. Contains 2560 test audios.

Two kinds of Character Error Rates are computed:
1. CER on the best prediction outputted by Apple's ASR
2. The minimum CER on all prediction candidates outputted by Apple's ASR. Or in other words, I pick the prediction candidate that has the closest levenshtein distance to the reference sentence and calculate its CER.

Here are the results obtained using macOS Ventura 13.6 (22G120) on a M1 Max macBook Pro:
| Dataset          | Best Predictions CER Score  | Closest Predictions CER Score |
|------------------|-----------------------------|-------------------------------|
| Common Voice 11  | 13.846%                     | 9.604%                        |
| Common Voice 15  | 13.988%                     | 9.677%                        |

# Footnote
For the zh-HK test set, we changed the ASCII double quotes to Chinese-style double quotes because of TSV parsing issues:

common_voice_zh-HK_23107405.mp3   同事找來一對桌上"小"揚聲器 => 同事找來一對桌上“小”揚聲器
