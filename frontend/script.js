async function submitForm() {
    const fileInput = document.getElementById("resumeFile");
    const jdElement = document.getElementById("jobDescription");
    const resultDiv = document.getElementById("result");

    if(!fileInput.files.length || !jdElement.value) {
        alert("Please upload resume and paste job description");
        return;
    }

    resultDiv.innerHTML = `<p class="loading">Analyzing resume...</p>`;


    const formData = new FormData();
    formData.append("resume", fileInput.files[0]);
    formData.append("job_description", jdElement.value);

    try {
        const response = await fetch("https://resume-matcher-2-nq7d.onrender.com/match", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    let scoreColor = "red";
    if(data.final_hybrid_score >= 75) scoreColor = "green";
    else if(data.final_hybrid_score >= 50) scoreColor = "yellow";


    resultDiv.innerHTML = `
        <div class = "score ${scoreColor}">
             Final Hybrid Score: ${data.final_hybrid_score}%
        </div>
        <p><strong>TF-IDF Score:</strong> ${data.tfidf_score}%</p>
        <p><strong>Skill Score:</strong> ${data.skill_score}%</p>
        <p><strong>Matching Skills:</strong> ${data.matching_skills.join(", ")}</p>
        <p><strong>Missing Skills:</strong> ${data.missing_skills.join(", ")}</p>
    `;
} catch(error) {
    resultDiv.innerHTML = `<p class="red">Error analyzing resume. Please try again.</p>`;
 }
}
