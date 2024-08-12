# Comprehensive Guide to the Translation Tool

## Outline
1. Introduction
   - Purpose and Promise
   - Target Audience
2. High-Level Overview
   - What is the Translation Tool?
   - Key Features
3. Technical Deep Dive
   - Architecture Overview
   - Code Walkthrough
     - HTML Structure
     - JavaScript Functionality
4. Conclusion
   - Key Takeaways
   - Call to Action

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
- **Automatic Language Detection:** Utilizes the `franc` library for accurate language identification.
- **Local Storage Capabilities:** Saves user preferences for a personalized experience.
- **Real-Time Translations:** Integrates with a translation API for immediate results.

## 3. Technical Deep Dive

### Architecture Overview
The Translation Tool is built using HTML, CSS (via Tailwind CSS), and JavaScript (with Alpine.js). The application is structured to provide a responsive and interactive user experience.

### Code Walkthrough

#### HTML Structure
The HTML file (`index.html`) serves as the backbone of the application. It includes essential elements such as text areas for input and output, buttons for actions, and sections for settings.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💱 Translation Tool</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body>
    <div x-data="app()" x-init="loadFromLocalStorage()" class="max-w-3xl mx-auto p-8">
        <h1 class="text-2xl font-bold">💱 Translation Tool Demo</h1>
        <!-- Form and Instructions -->
        <details class="mt-8 bg-yellow-100 shadow-md rounded-lg p-6 mb-6">
            <summary class="font-bold text-gray-800">How to fill in the form 📝</summary>
            <p class="text-gray-600 mt-4">To make your offer findable in all languages, please:</p>
            <ul class="list-disc pl-6 text-gray-600 mt-4">
                <li><strong>✍️ Always write full sentences</strong> (instead of just keywords).</li>
                <li><strong>🔠 Put specific terms</strong> such as product names, brands or technical terms in "quotations".</li>
                <li><strong>📚 Write out industry norms and abbreviations in full</strong>.</li>
                <li><strong>🌐 Use just one language</strong> in the input.</li>
            </ul>
        </details>
        <!-- Input and Output Areas -->
        <div class="mt-8">
            <label for="content" class="block text-gray-700 font-bold mb-2">Content (product or company)</label>
            <textarea id="content" x-model="content" rows="8" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"></textarea>
            <p class="text-gray-500 text-sm">Detected language: <span id="languageDetected"></span></p>
        </div>
        <div class="mt-8">
            <label for="language_target" class="block text-gray-700 font-bold mb-2">Target Language</label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" list="target_languages" type="text" name="language_target" id="language_target" x-model="language_target">
            <datalist id="target_languages">
                <option value="English">English</option>
                <option value="Turkish">Turkish</option>
                <option value="German">German</option>
            </datalist>
        </div>
        <button @click="savePrompt()" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4" id="saveTranslation">
            Translate
        </button>
        <div class="mt-4">
            <label for="content_translation" class="block text-gray-700 font-bold mb-2">Translated Content</label>
            <textarea id="content_translation" x-model="content_translation" rows="8" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"></textarea>
        </div>
    </div>
</body>
</html>
```

#### JavaScript Functionality
The JavaScript code, embedded within the HTML, handles the core functionality of the application, including language detection and API interaction.

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

The `franc` library is used to detect the language of the input text. The detected language is then displayed to the user, providing immediate feedback.

### API Integration
The application integrates with a translation API to perform real-time translations. The API key and model are stored locally for user convenience.

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

