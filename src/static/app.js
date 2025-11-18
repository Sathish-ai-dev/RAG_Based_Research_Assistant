const messagesEl = document.querySelector("#messages");
const statusEl = document.querySelector("#status");
const formEl = document.querySelector("#chat-form");
const questionInput = document.querySelector("#question");
const submitBtn = document.querySelector("#submit-btn");
const uploadForm = document.querySelector("#upload-form");
const fileInput = document.querySelector("#document-file");
const uploadBtn = document.querySelector("#upload-btn");
const uploadStatus = document.querySelector("#upload-status");

const startMessages = [
  {
    role: "assistant",
    content: "Ask me anything about the research documents in your workspace.",
  },
];

function createMessageBubble({ role, content }) {
  const wrapper = document.createElement("article");
  wrapper.className = `message ${role}`;

  const heading = document.createElement("h3");
  heading.textContent = role === "assistant" ? "Assistant" : "You";

  const body = document.createElement("p");
  body.textContent = content;

  wrapper.appendChild(heading);
  wrapper.appendChild(body);

  return wrapper;
}

function renderMessages(messages) {
  messagesEl.innerHTML = "";
  messages.forEach((msg) => {
    messagesEl.appendChild(createMessageBubble(msg));
  });
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.textContent = isLoading ? "Thinking..." : "Send";
  statusEl.textContent = isLoading
    ? "Generating answer..."
    : "Ask specific research questions to get grounded answers.";
}

async function sendQuestion(question, messages) {
  const response = await fetch("/api/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    let detail = "Unexpected error.";
    try {
      const data = await response.json();
      detail = data.detail || detail;
    } catch {
      detail = response.statusText;
    }
    throw new Error(detail);
  }

  return response.json();
}

function showError(error) {
  const errorMessage = {
    role: "assistant",
    content: `⚠️ ${error.message}`,
  };
  return errorMessage;
}

renderMessages(startMessages);

questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    formEl.requestSubmit();
  }
});

formEl.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = questionInput.value.trim();
  if (!question) return;

  const currentMessages = [
    ...Array.from(messagesEl.children).map((node) => ({
      role: node.classList.contains("assistant") ? "assistant" : "user",
      content: node.querySelector("p")?.textContent ?? "",
    })),
    { role: "user", content: question },
  ];

  renderMessages(currentMessages);
  questionInput.value = "";
  setLoading(true);

  try {
    const data = await sendQuestion(question);
    currentMessages.push({ role: "assistant", content: data.answer });
    renderMessages(currentMessages);
  } catch (error) {
    currentMessages.push(showError(error));
    renderMessages(currentMessages);
  } finally {
    setLoading(false);
  }
});

async function handleUpload(event) {
  event.preventDefault();
  if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
    if (uploadStatus) {
      uploadStatus.textContent = "Please select a .txt file before uploading.";
    }
    return;
  }

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  if (uploadBtn) {
    uploadBtn.disabled = true;
    uploadBtn.textContent = "Uploading...";
  }
  if (uploadStatus) {
    uploadStatus.textContent = `Uploading '${file.name}'...`;
  }

  try {
    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });
    let data = null;
    try {
      data = await response.json();
    } catch {
      // ignore json errors
    }
    if (!response.ok) {
      throw new Error(data?.detail || "Upload failed. Please try again.");
    }

    if (uploadStatus) {
      uploadStatus.textContent =
        data?.message || `Uploaded '${file.name}' successfully.`;
    }
    if (fileInput) {
      fileInput.value = "";
    }
  } catch (error) {
    if (uploadStatus) {
      uploadStatus.textContent = `⚠️ ${error.message}`;
    }
  } finally {
    if (uploadBtn) {
      uploadBtn.disabled = false;
      uploadBtn.textContent = "Upload";
    }
  }
}

if (uploadForm) {
  uploadForm.addEventListener("submit", handleUpload);
}

