window.onload = () => {
    const list = document.getElementById('importantQuestionsList');
    const questions = JSON.parse(localStorage.getItem('importantQuestions')) || [];

    if (questions.length === 0) {
        const li = document.createElement('li');
        li.className = 'no-questions';
        li.innerText = 'No important questions found based on keywords.';
        list.appendChild(li);
    } else {
        questions.forEach((q, idx) => {
            const li = document.createElement('li');
            li.className = 'question-item';
            li.innerHTML = `<span class="q-num">${idx + 1}.</span> ${q}`;
            list.appendChild(li);
        });
    }
};
