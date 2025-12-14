// frontend/src/features/userProfile/ViewUserProfilePage.jsx

import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getUserById } from "@/api/otherUser";

export default function ViewUserProfilePage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await getUserById(id);
        setUser(data);
      } catch (err) {
        setError(err.message);
      }
    }
    load();
  }, [id]);

  // Error UI
  if (error) {
    return (
      <div className="text-red-400 p-10 text-center">
        {error.includes("404")
          ? "User not found."
          : "Failed to load user profile."}
      </div>
    );
  }

  // Loading UI
  if (!user) {
    return (
      <div className="flex justify-center p-10 text-white">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-white"></div>
      </div>
    );
  }

  return (
    <div className="flex justify-center p-10 text-white">
      <div className="w-[600px] bg-gray-900 p-8 rounded-xl shadow-xl">

        {/* Back Button */}
        <button
          onClick={() => navigate(-1)}
          className="text-blue-400 hover:underline mb-4"
        >
          ← Back
        </button>

        {/* User Info */}
        <div className="flex items-center gap-4 mb-6">
          <div className="w-20 h-20 rounded-full bg-gray-700" />
          <div>
            <h1 className="text-2xl font-bold">
              {user.first_name} {user.last_name}
            </h1>
            <p className="text-gray-400">{user.email}</p>

            <p className="text-gray-400">
              City: {user.rotation_city?.name || "Unknown"}
            </p>
          </div>
        </div>

        <h2 className="text-xl font-semibold mb-3">Items</h2>

        {/* No items in backend schema */}
        <p className="text-gray-400">
          Items are not included in the backend response.
        </p>

      </div>
    </div>
  );
}

