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

  // Manejo de cambio en el año
  const handleYearChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setYear(e.target.value);
  };

  // Manejo de cambio en el mes
  const handleMonthChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setMonth(e.target.value);
  };

  return (
    <div className="p-6 bg-white shadow-md rounded-lg max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-4 text-gray-600">
        Download Dataset
      </h2>

      <select
        value={year}
        onChange={handleYearChange}
        className="border p-2 rounded w-full mb-2 text-gray-600"
      >
        <option value="">Year</option>
        {Array.from(
          { length: 2025 - 2013 + 1 },
          (_, index) => 2013 + index
        ).map((yearOption) => (
          <option key={yearOption} value={yearOption.toString()}>
            {yearOption}
          </option>
        ))}
      </select>

      <select
        value={month}
        onChange={handleMonthChange}
        className="border p-2 rounded w-full mb-4 text-gray-600"
      >
        <option value="">Month (optional)</option>
        <option value="1">January</option>
        <option value="2">February</option>
        <option value="3">March</option>
        <option value="4">April</option>
        <option value="5">May</option>
        <option value="6">June</option>
        <option value="7">July</option>
        <option value="8">August</option>
        <option value="9">September</option>
        <option value="10">October</option>
        <option value="11">November</option>
        <option value="12">December</option>
      </select>

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
