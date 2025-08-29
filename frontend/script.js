const API_URL = "/api/reviews"; // Azure Static Web App automatically maps backend

document.getElementById("reviewForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const movie = document.getElementById("movie").value;
  const rating = document.getElementById("rating").value;
  const comment = document.getElementById("comment").value;

  await fetch(API_URL, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ movie, rating, comment })
  });

  loadReviews();
});

async function loadReviews() {
  const res = await fetch(API_URL);
  const data = await res.json();
  document.getElementById("reviews").innerHTML = data.map(r =>
    `<p><b>${r.movie}</b> ⭐${r.rating}/5 <br>${r.comment}</p>`
  ).join("");
}

loadReviews();
