"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { getDataset } from "@/services/datasetService";

type FormData = {
  year: string;
  month?: string;
};

const Form = () => {
  const { register, handleSubmit } = useForm<FormData>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = async (data: FormData) => {
    setLoading(true);
    setError("");

    try {
      await getDataset(data.year, data.month);
    } catch (e) {
      console.error(e);
      setError("Error downloading dataset");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white shadow-lg rounded-xl">
      <h2 className="text-2xl font-bold text-center text-gray-800 mb-4">
        CitiBike dataset
      </h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-gray-600">Year*</label>
          <input
            type="number"
            {...register("year", { required: true })}
            className="w-full border p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 text-gray-600"
          />
        </div>
        <div>
          <label className="block text-gray-600">Month</label>
          <input
            type="number"
            {...register("month")}
            className="w-full border p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 text-gray-600"
          />
        </div>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-3 rounded-md hover:bg-blue-700 transition-all"
          disabled={loading}
        >
          {loading ? "Downloading..." : "Download"}
        </button>
      </form>
    </div>
  );
};

export default Form;
