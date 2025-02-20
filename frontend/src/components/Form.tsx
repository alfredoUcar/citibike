"use client";
import { useState } from "react";
import { getDataset } from "../services/datasetService";

export default function DownloadDataset() {
  const [year, setYear] = useState("");
  const [month, setMonth] = useState("");
  const [progress, setProgress] = useState<number | null>(null);

  const handleDownload = async () => {
    setProgress(0); // Show progress bar
    await getDataset(year, month, (p) => setProgress(p));
    setProgress(null); // Hide progress bar after completion
  };

  return (
    <div className="p-6 bg-white shadow-md rounded-lg max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-4 text-gray-600">
        Download Dataset
      </h2>
      <input
        type="text"
        placeholder="Year"
        value={year}
        onChange={(e) => setYear(e.target.value)}
        className="border p-2 rounded w-full mb-2 text-gray-600"
      />
      <input
        type="text"
        placeholder="Month (optional)"
        value={month}
        onChange={(e) => setMonth(e.target.value)}
        className="border p-2 rounded w-full mb-4 text-gray-600"
      />
      <button
        onClick={handleDownload}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 w-full"
      >
        Download
      </button>
      {progress !== null && (
        <div className="mt-4">
          <p className="text-sm text-gray-600">Downloading... {progress}%</p>
          <div className="w-full bg-gray-200 h-2 rounded mt-1">
            <div
              className="bg-blue-500 h-2 rounded"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
