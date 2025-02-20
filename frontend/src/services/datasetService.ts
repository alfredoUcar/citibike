import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const getDataset = async (year: string, month?: string) => {
  const params = new URLSearchParams({ year });
  if (month) params.append("month", month);

  const datasetUrl = `${API_URL}/dataset?${params.toString()}`;
  console.log("Request dataset", { datasetUrl });
  const response = await axios.get(datasetUrl, {
    responseType: "blob",
  });

  // Download file
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute(
    "download",
    `dataset_${year}${month ? `_${month}` : ""}.zip`
  );
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
