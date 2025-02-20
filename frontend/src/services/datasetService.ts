import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const getDataset = async (
  year: string,
  month?: string,
  onProgress?: (progress: number) => void
) => {
  const params = new URLSearchParams({ year });
  if (month) params.append("month", month);

  const response = await axios.get(`${API_URL}/dataset?${params.toString()}`, {
    responseType: "blob",
    onDownloadProgress: (progressEvent) => {
      if (progressEvent.total) {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        if (onProgress) onProgress(percentCompleted);
      }
    },
  });

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
