document.getElementById('processBtn').addEventListener('click', () => {
    const files = document.getElementById('fileInput').files;
    if (files.length === 0) {
        alert('Please upload at least one Word document (.docx)');
        return;
    }

    const promises = [];
    for (let i = 0; i < files.length; i++) {
        if (!files[i].name.endsWith('.docx')) {
            alert('Invalid file detected. Please upload only .docx files.');
            return;
        }
        promises.push(readFile(files[i]));
    }

    Promise.all(promises).then(results => {
        const allText = results.join(" ");
        const importantQuestions = extractImportantQuestions(allText);
        localStorage.setItem('importantQuestions', JSON.stringify(importantQuestions));
        window.location.href = "results.html";
    });
});

function readFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = function(event) {
            mammoth.extractRawText({ arrayBuffer: event.target.result })
                .then(result => resolve(result.value))
                .catch(err => reject(err));
        };
        reader.readAsArrayBuffer(file);
    });
}

function extractImportantQuestions(text) {
    const lines = text.split(/[\n.?!]\s+/);
    const results = [];

    lines.forEach(line => {
        const lowerLine = line.toLowerCase();
        let keywordMatches = 0;
        let keywordCounts = {};

        keywords.forEach(kw => {
            const count = (lowerLine.match(new RegExp(kw, "g")) || []).length;
            if (count > 0) {
                keywordMatches++;
                keywordCounts[kw] = count;
            }
        });

        if (keywordMatches >= 2 || Object.values(keywordCounts).some(cnt => cnt >= 2)) {
            results.push(line.trim());
        }
    });

    return results;
}
