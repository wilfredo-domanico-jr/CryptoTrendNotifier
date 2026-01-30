// Initialize AOS animations
AOS.init({
  duration: 800,
  easing: "ease-in-out",
  once: true,
});

// Create animated particles
function createParticles() {
  const particlesContainer = document.getElementById("particles");
  const particleCount = 20;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement("div");
    particle.className = "particle";
    particle.style.width = Math.random() * 100 + 50 + "px";
    particle.style.height = particle.style.width;
    particle.style.left = Math.random() * 100 + "%";
    particle.style.top = Math.random() * 100 + "%";
    particle.style.animationDelay = Math.random() * 20 + "s";
    particle.style.animationDuration = Math.random() * 20 + 15 + "s";
    particlesContainer.appendChild(particle);
  }
}

createParticles();

// Search functionality
document.getElementById("searchInput").addEventListener("input", function (e) {
  const searchTerm = e.target.value.toLowerCase();
  const rows = document.querySelectorAll("#cryptoTableBody tr");

  rows.forEach((row) => {
    const coin = row.dataset.coin.toLowerCase();
    if (coin.includes(searchTerm)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
});

// Create chart
const ctx = document.getElementById("trendChart").getContext("2d");

// Extract data from table for chart
const rows = document.querySelectorAll("#cryptoTableBody tr");
const labels = [];
const currentPrices = [];
const predictedPrices = [];

rows.forEach((row) => {
  const coin = row.dataset.coin;
  const currentPrice = parseFloat(
    row.querySelector(".price").textContent.replace("$", ""),
  );
  const predictionElement = row.querySelector(".prediction-value");
  const predictedPrice = predictionElement
    ? parseFloat(predictionElement.textContent.replace("$", ""))
    : currentPrice;

  labels.push(coin);
  currentPrices.push(currentPrice);
  predictedPrices.push(predictedPrice);
});

const chart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: labels,
    datasets: [
      {
        label: "Current Price",
        data: currentPrices,
        backgroundColor: "rgba(99, 102, 241, 0.8)",
        borderColor: "rgba(99, 102, 241, 1)",
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      },
      {
        label: "Predicted Price",
        data: predictedPrices,
        backgroundColor: "rgba(34, 197, 94, 0.8)",
        borderColor: "rgba(34, 197, 94, 1)",
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: true,
    interaction: {
      mode: "index",
      intersect: false,
    },
    plugins: {
      legend: {
        display: true,
        position: "top",
        labels: {
          color: "#f1f5f9",
          font: {
            family: "Inter",
            size: 12,
            weight: 600,
          },
          padding: 15,
          usePointStyle: true,
          pointStyle: "circle",
        },
      },
      tooltip: {
        backgroundColor: "rgba(15, 23, 42, 0.95)",
        titleColor: "#f1f5f9",
        bodyColor: "#94a3b8",
        borderColor: "rgba(99, 102, 241, 0.5)",
        borderWidth: 1,
        padding: 12,
        displayColors: true,
        callbacks: {
          label: function (context) {
            return context.dataset.label + ": $" + context.parsed.y.toFixed(2);
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: "rgba(51, 65, 85, 0.3)",
          drawBorder: false,
        },
        ticks: {
          color: "#94a3b8",
          font: {
            family: "Inter",
            size: 11,
          },
          callback: function (value) {
            return "$" + value.toFixed(0);
          },
        },
      },
      x: {
        grid: {
          display: false,
          drawBorder: false,
        },
        ticks: {
          color: "#94a3b8",
          font: {
            family: "Inter",
            size: 11,
            weight: 600,
          },
        },
      },
    },
  },
});

// Auto-update timestamp
function updateTimestamp() {
  const now = new Date();
  const timeString = now.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
  document.getElementById("timestamp").textContent = timeString;
}

updateTimestamp();
setInterval(updateTimestamp, 1000);

// Add hover effects to table rows
document.querySelectorAll("#cryptoTableBody tr").forEach((row) => {
  row.addEventListener("click", function () {
    const coin = this.dataset.coin;
    alert(`Detailed analytics for ${coin} coming soon!`);
  });
});
