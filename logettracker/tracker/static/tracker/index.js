document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll('.card');

  cards.forEach((card, _) => {
    const randomDuration = Math.random() * 25 + 5; // between 5 and 30 seconds
    card.style.animationDuration = `${randomDuration}s`;
  });
});