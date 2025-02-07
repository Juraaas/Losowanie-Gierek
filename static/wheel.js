class Wheel {
    constructor(center, radius, games = []) {
        this.center = center;
        this.radius = radius;
        this.games = games.length > 0 ? games : Array(8).fill({ nazwa: "I tak zagramy w Isaac" });
        this.angle = 0;
    }

    updateGames(newGames) {
        let oldSliceCount = this.games.length;
        let newSliceCount = newGames.length > 0 ? newGames.length : 8;

        if (oldSliceCount !== newSliceCount) {
            let sliceRatio = oldSliceCount / newSliceCount;
            this.angle *= sliceRatio;
        }

        this.games = newGames.length > 0 ? newGames : Array(8).fill({ nazwa: " " });
        this.draw(ctx);
}

    draw(ctx) {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        const sliceCount = this.games.length;
        const colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "gray"];

        for (let i = 0; i < sliceCount; i++) {
            const startAngle = this.angle + (2 * Math.PI * i) / sliceCount;
            const endAngle = this.angle + (2 * Math.PI * (i + 1)) / sliceCount;

            ctx.beginPath();
            ctx.moveTo(this.center.x, this.center.y);
            ctx.arc(this.center.x, this.center.y, this.radius, startAngle, endAngle);
            ctx.fillStyle = colors[i % colors.length];
            ctx.fill();

            const textAngle = (startAngle + endAngle) / 2;
            ctx.fillStyle = "black";
            ctx.font = "16px Arial";
            ctx.textAlign = "center";
            ctx.fillText(
                this.games[i].nazwa,
                this.center.x + Math.cos(textAngle) * this.radius * 0.7,
                this.center.y + Math.sin(textAngle) * this.radius * 0.7
            );
        }

        // Rysowanie strzałki u góry koła
        ctx.fillStyle = "black";
        ctx.beginPath();
        ctx.moveTo(this.center.x, this.center.y - this.radius - 10);
        ctx.lineTo(this.center.x - 10, this.center.y - this.radius - 30);
        ctx.lineTo(this.center.x + 10, this.center.y - this.radius - 30);
        ctx.closePath();
        ctx.fill();
    }

    spin(callback) {
        if (this.games.every(game => game.nazwa === "Brak danych")) {
            alert("Nie można losować, koło jest puste.");
            return;
        }

        let totalSpins = Math.floor(Math.random() * 5 + 4);
        let finalAngle = Math.random() * (2 * Math.PI);
        let spinDuration = 3000;
        let startTime = null;

        const animate = (timestamp) => {
            if (!startTime) startTime = timestamp;
            let progress = timestamp - startTime;
            let ease = Math.min(progress / spinDuration, 1);

            // Użycie funkcji ease-out dla płynniejszego spowolnienia
            let easedProgress = 1 - Math.pow(1 - ease, 3);
            this.angle = totalSpins * 2 * Math.PI * easedProgress + finalAngle;

            this.draw(ctx);

            if (progress < spinDuration) {
                requestAnimationFrame(animate);
            } else {
                this.angle %= 2 * Math.PI;

                let sliceAngle = (2 * Math.PI) / this.games.length;
                let correctedAngle = (3 * Math.PI / 2 - this.angle) % (2 * Math.PI);
                if (correctedAngle < 0) correctedAngle += 2 * Math.PI;

                let selectedIndex = Math.floor(correctedAngle / sliceAngle) % this.games.length;
                let selectedGame = this.games[selectedIndex];

                document.getElementById("selected_game").innerText = "Wylosowana gra: " + selectedGame.nazwa;
                if (callback) callback(selectedGame);
    }
};

        requestAnimationFrame(animate);
    }

    finalizeSpin(callback) {
        const sliceCount = this.games.length;
        const anglePerSlice = (2 * Math.PI) / sliceCount;

        let correctedAngle = (3 * Math.PI / 2 - this.angle) % (2 * Math.PI);
        if (correctedAngle < 0) correctedAngle += 2 * Math.PI;

        let selectedIndex = Math.round(correctedAngle / anglePerSlice) % sliceCount;

        this.angle = (3 * Math.PI / 2) - selectedIndex * anglePerSlice;
        this.angle %= 2 * Math.PI;

        this.draw(ctx);
        callback(this.games[selectedIndex]);
    }
}