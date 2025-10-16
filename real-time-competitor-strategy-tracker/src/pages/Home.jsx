import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center text-center px-4">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">
        Welcome to ShopSmart
      </h1>
      <p className="text-gray-600 max-w-lg mb-6">
        Find your favorite products at the best prices. Shop smart, stay updated.
      </p>
      <div className="space-x-4">
        <Link
          to="/products"
          className="bg-amber-500 hover:bg-amber-600 text-white px-6 py-3 rounded-lg shadow transition"
        >
          Browse Products
        </Link>
        <Link
          to="/admin/login"
          className="border border-amber-500 text-amber-600 px-6 py-3 rounded-lg hover:bg-amber-50 transition"
        >
          Admin Login
        </Link>
      </div>
    </div>
  );
}
