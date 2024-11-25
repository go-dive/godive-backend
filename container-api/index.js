const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const port = 3000;

// Endpoint untuk mendapatkan semua desc
app.get("/api/descriptions", (req, res) => {
    fs.readFile(path.join(__dirname, "desc.json"), "utf8", (err, data) => {
        if (err) {
            return res.status(500).json({ error: "Error reading file" });
        }
        const descriptions = JSON.parse(data);
        res.json(descriptions.divingSpots);
        });
    });

// Endpoint untuk mendapatkan desc berdasarkan ID
app.get("/api/descriptions/:id", (req, res) => {
    const descriptionsId = parseInt(req.params.id);
    fs.readFile(path.join(__dirname, "desc.json"), "utf8", (err, data) => {
        if (err) {
            return res.status(500).json({ error: "Error reading file" });
    }
        const descriptions = JSON.parse(data).divingSpots;
        const desc = descriptions.find(desc => desc.id === descriptionsId);
        if (!desc) {
            return res.status(404).json({ error: "Description not found" });
        }
            res.json(desc);
        });
    });

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
