const form = document.getElementById("analyzeForm");
const loading = document.getElementById("loading");
const result = document.getElementById("result");

/*
  Backend and frontend are on the SAME domain
*/
const API_BASE_URL = "";

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    loading.classList.remove("hidden");
    result.classList.add("hidden");

    const crop = document.getElementById("crop").value;
    const language = document.getElementById("language").value;
    const imageFile = document.getElementById("image").files[0];

    if (!imageFile) {
        alert("Please upload an image.");
        loading.classList.add("hidden");
        return;
    }

    const formData = new FormData();
    formData.append("crop", crop);
    formData.append("language", language);
    formData.append("file", imageFile);

    try {
        const response = await fetch(`${API_BASE_URL}/analyze/image`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            // READ REAL BACKEND ERROR
            const errorText = await response.text();
            throw new Error(errorText);
        }

        const data = await response.json();

        document.getElementById("disease").innerText =
            data.disease?.disease || "Unknown";

        document.getElementById("confidence").innerText =
            data.disease?.confidence !== undefined
                ? (data.disease.confidence * 100).toFixed(1) + "%"
                : "N/A";

        document.getElementById("severity").innerText =
            data.severity
                ? `${data.severity.risk_level} (${data.severity.severity_percent}%)`
                : "N/A";

        document.getElementById("explanation").innerText =
            data.disease?.explanation || "No explanation available";

        const treatmentList = document.getElementById("treatment");
        treatmentList.innerHTML = "";
        (data.solution?.treatment || []).forEach(item => {
            const li = document.createElement("li");
            li.innerText = item;
            treatmentList.appendChild(li);
        });

        const preventionList = document.getElementById("prevention");
        preventionList.innerHTML = "";
        (data.solution?.prevention || []).forEach(item => {
            const li = document.createElement("li");
            li.innerText = item;
            preventionList.appendChild(li);
        });

        loading.classList.add("hidden");
        result.classList.remove("hidden");

    } catch (err) {
        loading.classList.add("hidden");

        //  SHOW EXACT BACKEND ERROR
        alert("Backend error:\n\n" + err.message);

        console.error("Analysis error (FULL):", err);
    }
});
