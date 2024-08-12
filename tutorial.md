# Comprehensive Guide to the Translation Tool

## 1. Introduction

### Purpose and Promise
The Translation Tool is designed to facilitate seamless translations for B2B e-commerce platforms. This guide will show you how to implement and utilize the tool effectively, offering both technical insights and business value.

### Target Audience
This guide is tailored for product leaders seeking to understand the tool's capabilities and software developers interested in its technical implementation.

## 2. High-Level Overview

### What is the Translation Tool?
The Translation Tool is a web-based application that allows users to input text in one language and receive a translated version in another. It leverages advanced language detection and translation APIs to ensure accuracy and contextual relevance.

### Key Features
- **User-Friendly Interface:** Simplifies text input and target language selection.
- **Automatic Language Detection:** Utilizes the `franc` Javascript library for accurate language identification.
- **Local Storage Capabilities:** Saves user preferences for a personalized experience.
- **Real-Time Translations:** Integrates with a translation API for immediate results.

## 3. Technical Deep Dive

### Architecture Overview
The Translation Tool is built using HTML, CSS (via Tailwind CSS), and JavaScript (with Alpine.js). The application is structured to provide a responsive and interactive user experience.

### Code Walkthrough

#### HTML Structure
The HTML file (`index.html`) serves as the backbone of the application. It includes essential elements such as text areas for input and output, buttons for actions, and sections for settings.

Key elements include:
- **Text Areas**: For inputting the text to be translated and displaying the translated text.
- **Buttons**: For triggering the translation process.
- **Settings Section**: For configuring API keys and models.

#### JavaScript Functionality
The JavaScript code, embedded within the HTML, handles the core functionality of the application, including language detection and API interaction.

Key functionalities include:
- **Language Detection**: Using the `franc` library to detect the language of the input text. This is crucial for ensuring the translation is accurate and contextually relevant.
- **Event Handling**: Listening for user actions, such as button clicks, to trigger the translation process.

```javascript
document.addEventListener('DOMContentLoaded', () => {
    const content = document.getElementById('content');
    const translateButton = document.getElementById('saveTranslation');
    const languageDetectedSpan = document.getElementById('languageDetected');

    translateButton.addEventListener('click', (event) => {
        event.preventDefault();
        const detectedLanguage = franc(content.value);
        console.log('Detected language code:', detectedLanguage);

        // Update the "languageDetected" span with the detected language
        languageDetectedSpan.innerHTML = detectedLanguage;
    });
});
```

### API Integration
The application integrates with a LLM API to perform real-time translations. The API key and model are stored locally for user convenience.

#### Prompt Explanation for Business Users
The prompt is a set of instructions that guides the translation tool on how to handle your text. Here’s what each rule means for your business:

1. **Natural Sounding Translations**: The tool aims to make translations sound as if they were originally written in the target language, ensuring they are smooth and easy to read.
2. **Attention to Nuance**: It captures subtle differences in meaning, so the translated text conveys the same message and tone as the original.
3. **Preserve Quoted Terms**: Any terms you put in double quotes, like product names or technical terms, will remain unchanged in the translation. This ensures brand consistency and accuracy.
4. **Company Name Consistency**: Your company name will never be translated, maintaining brand identity across languages.
5. **Use of Double Quotes**: The tool will only use double quotes for quotations, ensuring clarity and uniformity in the translated text.

These rules help maintain the integrity and effectiveness of your business communications across different languages.

```javascript
async savePrompt(detectedLanguage) {
    const system_prompt = `
        You are a helpful translator for a B2B e-commerce platform. Your task is to translate the following text while adhering to the following rules:
        1. Make the translation sound as natural as possible.
        2. Pay attention to nuance.
        3. Never translate terms that are enclosed in double straight quotation marks ("), even if the terms contain words that could be translated.
        4. You MUST NEVER translate any occurrences of the company name.
        5. You MUST only use double straight quotation marks (") for quotations.
    `;
    const user_prompt = `
      <input>
        <company_description>
        ${this.content}
        </company_description>
      </input>
        Translate the company description text from ${detectedLanguage} (ISO 639-3) to ${this.language_target} while following ALL rules above.
        Use JSON format in the format { "content": "{{TRANSLATED_TEXT}}" }. Return the unescaped raw JSON, nothing else, don't add Markdown.
    `;
    console.log(user_prompt);
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'X-Title': 'translation_tool',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: this.model,
            temperature: 0,
            messages: [{ role: 'system', content: system_prompt }, { role: 'user', content: user_prompt }]
        })
    });
    this.response = await response.json();
    try {
        const parsedResponse = JSON.parse(this.response.choices[0].message.content);
        this.content_translation = parsedResponse.content;
    } catch (error) {
        console.error('Error parsing response:', error);
    }
}
```

## 4. Conclusion

### Key Takeaways
- The Translation Tool offers a seamless experience for translating text in a B2B context.
- It combines user-friendly design with powerful language detection and translation capabilities.
- The tool is highly customizable, allowing users to save preferences and integrate with various APIs.

### Call to Action
Explore the Translation Tool and see how it can enhance your B2B e-commerce platform. Share your experiences and feedback to help us improve further.

This guide has provided a comprehensive overview of the Translation Tool, from its high-level features to its technical implementation. We hope it serves as a valuable resource for both product leaders and developers.

