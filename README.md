# 📊 PPT-AI: AI-Powered Presentation Generator

**PPT-AI** is an AI-driven chatbot that leverages a fine-tuned LLM to generate PowerPoint presentations effortlessly. Whether you need a step-by-step guided creation or a full presentation from a single instruction, PPT-AI streamlines the process, saving time and enhancing productivity.

## 🚀 Features

- 📌 Generate PowerPoint slides from a single prompt
- ⚡ Step-by-step interactive presentation building
- 🎨 Customizable slide content and design suggestions
- 🔄 Supports various topics and industries

## 🛠 How It Works

To develop **PPT-AI**, I created a custom API that implements the `python-pptx` library to generate PowerPoint presentations. This API simplifies the complexity of working with the python-pptx library by abstracting the logic into high-level functions. The AI model learns to call the appropriate API functions and pass the required parameters to generate presentations accurately.

### 📚 Dataset Creation

A dataset was constructed containing pairs of **(prompt, API function calls)**, allowing the model to learn how to generate presentations in different ways:

1. **Step-by-Step Presentation Creation:** The dataset includes interactions where each instruction adds or modifies a slide incrementally.
   
   **Example:**
   ```plaintext
   Create a title slide about the history of guitars with a subtitle.
   Add a slide and give a description about guitars.
   Add a slide with a list of types of guitars and include sub-bullet points with examples of the genres where the guitar is used.
   Add an image slide that includes a picture of a person playing an electric guitar.
   Add a conclusion slide that talks about the benefits of playing guitar.
   ```
   
2. **Full Presentation Generation with a Single Prompt:** The dataset also contains examples where a single prompt describes the entire presentation, and the output consists of the necessary API function calls to generate the slides.
   
   **Example:**
   ```plaintext
   Create a detailed presentation about 'Famous Historical Figures' with a title slide, a slide listing the topics that will be covered (with subpoints), a slide about the life of Alexander the Great with an image, a slide about Cleopatra with an image, a listing slide about Napoleon Bonaparte with subpoints, and a conclusion slide summarizing the impact of these figures on history.
   ```

### 🤖 Model Fine-Tuning

Using the dataset, I fine-tuned the **Qwen2.5-7B-Instruct** model to learn how to:
- Generate PowerPoint presentations step by step.
- Modify existing slides dynamically.
- Add images and structured content.
- Create a full presentation from a single detailed instruction.

### 🖼️ Image Generation with Stable Diffusion

In addition to text-based slide generation, PPT-AI integrates with the Stable Diffusion API to generate images dynamically. When the AI model detects a request for an image slide, it:

1. Calls the Stable Diffusion API to generate a relevant image based on the prompt.

2. Retrieves the generated image and embeds it into the corresponding PowerPoint slide.

This feature enhances presentations by automating the process of adding visuals, making them more engaging and informative.

### 🖥 User Interface

I implemented a **Streamlit-based graphical interface**, allowing users to interact with the chatbot and generate presentations with real-time slide previews.

## 🛠 Installation & Execution

Follow these steps to run **PPT-AI** locally using **Streamlit**:

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Engleonardorm7/PPT-AI-AI-Powered-Presentation-Generator
```

### 2️⃣ Navigate to the project directory

```bash
cd PPT-AI/PerfectModel
```

### 3️⃣ Install dependencies

If you haven’t installed the required Python libraries, run:

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application with Streamlit

```bash
streamlit run interface.py
```

Now, open the provided URL in your browser and start generating presentations with AI! 🎉

## 📩 Future Improvements

- 🧠 Enhancing model accuracy with more diverse datasets
- 🌐 Expanding API functionality to support different presentation styles
- 🎭 Adding more customization options (themes, animations, transitions)



