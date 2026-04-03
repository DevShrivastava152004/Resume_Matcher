async function submitForm() {
    const fileInput = document.getElementById("resumeFile");
    const jdElement = document.getElementById("jobDescription");
    const resultDiv = document.getElementById("result");
    const loadingDiv = document.getElementById("loading");

    if (!fileInput.files.length || !jdElement.value.trim()) {
        alert("Please upload resume and paste job description");
        return;
    }

    loadingDiv.style.display = "block";
    resultDiv.innerHTML = "";

    const formData = new FormData();
    formData.append("resume", fileInput.files[0]);
    formData.append("job_description", jdElement.value);

    try {
        // 🔥 SWITCH HERE if testing locally
        const API_URL = "https://resume-matcher-lizq.onrender.com/match";
        // const API_URL = "http://127.0.0.1:8000/match";

        const response = await fetch(API_URL, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Server Error:", errorText);
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        console.log("API RESPONSE:", data);

        // 🔥 Safe parsing
        const finalScore = data.final_hybrid_score ?? 0;
        const dlScore = data.dl_score ?? 0;
        const skillScore = data.skill_score ?? 0;
        const matchingSkills = data.matching_skills || [];
        const missingSkills = data.missing_skills || [];
        const highPriority = data.high_priority_missing || [];

        // 🎯 Score color logic
        let scoreColor = "red";
        if (finalScore >= 75) scoreColor = "green";
        else if (finalScore >= 50) scoreColor = "yellow";

        loadingDiv.style.display = "none";

        resultDiv.innerHTML = `
            <div class="score ${scoreColor}">
                Final Score: ${finalScore}%
            </div>

            <p><strong>DL Score:</strong> ${dlScore}%</p>
            <p><strong>Skill Score:</strong> ${skillScore}%</p>

            <hr/>

            <p><strong>Matching Skills:</strong></p>
            <div class="skills">
                ${matchingSkills.length 
                    ? matchingSkills.map(s => `<span class="match">${s}</span>`).join("") 
                    : "None"}
            </div>

            <p><strong>Missing Skills:</strong></p>
            <div class="skills">
                ${missingSkills.length 
                    ? missingSkills.map(s => `<span class="miss">${s}</span>`).join("") 
                    : "None"}
            </div>

            <hr/>

            <p><strong>Top Missing Skills (Improve these first):</strong></p>
            <div class="skills">
                ${highPriority.length 
                    ? highPriority.map(s => `<span class="miss">${s}</span>`).join("") 
                    : "None"}
            </div>
        `;

    } catch (error) {
        console.error("FULL ERROR:", error);
        loadingDiv.style.display = "none";

        resultDiv.innerHTML = `
            <p class="red"><strong>Error analyzing resume</strong></p>
            <p>${error.message}</p>
            <p>Check console (F12) for details</p>
        `;
    }
}