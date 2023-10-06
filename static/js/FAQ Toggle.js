const questions = document.querySelectorAll(".FAQ-question");

questions.forEach((question) => {
	question.addEventListener("click", () => {
		const answer = question.nextElementSibling;
		const isAnswerVisible = getComputedStyle(answer).display !== "none";

		if (isAnswerVisible) {
			answer.style.display = "none";
		} else {
			answer.style.display = "block";
		}
	});
});
