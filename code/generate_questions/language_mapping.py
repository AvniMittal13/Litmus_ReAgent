# Similar language mapping - groups of similar languages
SIMILAR_LANGUAGES_MAPPING = {
    # Germanic languages
    "German": ["Dutch", "English", "Afrikaans", "Norwegian", "Swedish", "Danish"],
    "Dutch": ["German", "English", "Afrikaans", "Flemish"],
    "English": ["German", "Dutch", "Afrikaans"],
    "Afrikaans": ["Dutch", "German", "English"],
    "Norwegian": ["Swedish", "Danish", "German", "English"],
    "Swedish": ["Norwegian", "Danish", "German", "English"],
    "Danish": ["Norwegian", "Swedish", "German", "English"],
    "Flemish": ["Dutch", "German"],
    
    # Romance languages
    "Spanish": ["Portuguese", "Italian", "French", "Catalan", "Galician"],
    "Portuguese": ["Spanish", "Italian", "French", "Galician"],
    "Italian": ["Spanish", "Portuguese", "French", "Romanian"],
    "French": ["Spanish", "Portuguese", "Italian", "Romanian"],
    "Romanian": ["Italian", "French"],
    "Catalan": ["Spanish", "French", "Italian"],
    "Galician": ["Spanish", "Portuguese"],
    
    # Slavic languages
    "Russian": ["Ukrainian", "Bulgarian", "Serbian", "Croatian", "Polish", "Czech", "Slovak"],
    "Ukrainian": ["Russian", "Polish", "Bulgarian"],
    "Bulgarian": ["Russian", "Ukrainian", "Serbian", "Macedonian"],
    "Serbian": ["Croatian", "Bulgarian", "Russian", "Macedonian"],
    "Croatian": ["Serbian", "Slovenian", "Russian"],
    "Polish": ["Russian", "Ukrainian", "Czech", "Slovak"],
    "Czech": ["Slovak", "Polish", "Russian"],
    "Slovak": ["Czech", "Polish", "Russian"],
    "Slovenian": ["Croatian", "Serbian"],
    "Macedonian": ["Bulgarian", "Serbian"],
    
    # Sino-Tibetan languages
    "Chinese": ["Tibetan", "Burmese"],
    "Tibetan": ["Chinese", "Burmese"],
    "Burmese": ["Chinese", "Tibetan"],
    
    # Indo-Aryan languages
    "Hindi": ["Urdu", "Bengali", "Punjabi", "Gujarati", "Marathi", "Nepali", "Sinhala"],
    "Urdu": ["Hindi", "Punjabi", "Bengali", "Sinhala"],
    "Bengali": ["Hindi", "Urdu", "Assamese", "Sinhala"],
    "Punjabi": ["Hindi", "Urdu", "Sinhala"],
    "Gujarati": ["Hindi", "Marathi", "Sinhala"],
    "Marathi": ["Hindi", "Gujarati", "Sinhala"],
    "Nepali": ["Hindi", "Sinhala"],
    "Assamese": ["Bengali", "Hindi", "Sinhala"],
    "Sinhala": ["Hindi", "Bengali", "Urdu", "Nepali", "Assamese"],
    
    # Dravidian languages
    "Tamil": ["Telugu", "Malayalam", "Kannada"],
    "Telugu": ["Tamil", "Kannada", "Malayalam"],
    "Malayalam": ["Tamil", "Telugu", "Kannada"],
    "Kannada": ["Tamil", "Telugu", "Malayalam"],
    
    # Semitic languages
    "Arabic": ["Hebrew", "Amharic"],
    "Hebrew": ["Arabic"],
    "Amharic": ["Arabic", "Tigrinya"],
    "Tigrinya": ["Amharic"],
    
    # Turkic languages
    "Turkish": ["Azerbaijani", "Kazakh", "Uzbek", "Kyrgyz", "Turkmen"],
    "Azerbaijani": ["Turkish", "Turkmen"],
    "Kazakh": ["Turkish", "Uzbek", "Kyrgyz"],
    "Uzbek": ["Turkish", "Kazakh", "Kyrgyz"],
    "Kyrgyz": ["Turkish", "Kazakh", "Uzbek"],
    "Turkmen": ["Turkish", "Azerbaijani"],
    
    # Niger-Congo languages
    "Swahili": ["Yoruba", "Igbo", "Hausa"],
    "Yoruba": ["Igbo", "Swahili", "Hausa"],
    "Igbo": ["Yoruba", "Swahili", "Hausa"],
    "Hausa": ["Yoruba", "Igbo", "Swahili"],
    
    # Austro-Asiatic languages
    "Vietnamese": ["Khmer"],
    "Khmer": ["Vietnamese"],
    
    # Austronesian languages
    "Indonesian": ["Malay", "Tagalog", "Javanese"],
    "Malay": ["Indonesian", "Javanese"],
    "Tagalog": ["Indonesian", "Cebuano"],
    "Javanese": ["Indonesian", "Malay"],
    "Cebuano": ["Tagalog"],
    
    # Celtic languages
    "Irish": ["Welsh", "Scottish Gaelic"],
    "Welsh": ["Irish", "Scottish Gaelic"],
    "Scottish Gaelic": ["Irish", "Welsh"],
    
    # Finno-Ugric languages
    "Finnish": ["Estonian", "Hungarian"],
    "Estonian": ["Finnish", "Latvian", "Lithuanian"],
    "Hungarian": ["Finnish"],
    
    # Baltic languages
    "Latvian": ["Lithuanian", "Estonian"],
    "Lithuanian": ["Latvian", "Estonian"],
    
    # Other language groups
    "Persian": ["Pashto", "Kurdish"],
    "Pashto": ["Persian", "Kurdish"],
    "Kurdish": ["Persian", "Pashto"],
    
    "Greek": ["Armenian"],
    "Armenian": ["Greek"],
    
    "Korean": ["Japanese"],
    "Japanese": ["Korean"],
    
    "Thai": ["Lao"],
    "Lao": ["Thai"],
    
    "Mongolian": ["Kazakh"],
    
    "Albanian": ["Macedonian"],
    
    "Georgian": ["Armenian"],
}
