import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getUserById } from "@/api/otherUser";
import { Card, CardContent } from "@/shared/components/ui/card";
import { Button } from "@/shared/components/ui/button";

export default function ViewUserProfilePage() {
  const { id } = useParams();
  const [user, setUser] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await getUserById(id);
        setUser(data);
      } catch (err) {
        console.error("Failed to load user", err);
      }
    }
    load();
  }, [id]);

  if (!user) return <div className="text-white p-10">Loading...</div>;

  return (
    <div className="flex justify-center p-10 text-white">
      <div className="w-[600px] bg-gray-900 p-8 rounded-xl shadow-xl">

        <div className="flex items-center gap-4 mb-6">
          <div className="w-20 h-20 rounded-full bg-gray-700" />
          <div>
            <h1 className="text-2xl font-bold">
              {user.first_name} {user.last_name}
            </h1>
            <p className="text-gray-400">{user.email}</p>
            <p className="text-gray-400">City: {user.rotation_city}</p>
          </div>
        </div>

        <h2 className="text-xl font-semibold mb-3">Items</h2>

        <div className="flex flex-col gap-3">
          {user.items?.length > 0 ? (
            user.items.map((item) => (
              <div
                key={item.item_id}
                className="bg-gray-800 p-4 rounded-lg flex justify-between"
              >
                <div>
                  <p className="font-semibold">{item.name}</p>
                  <p className="text-sm text-gray-400">
                    Location: {item.location}
                  </p>
                </div>

                <Button className="bg-blue-600">Request</Button>
              </div>
            ))
          ) : (
            <p className="text-gray-400">No items listed</p>
          )}
        </div>
      </div>
    </div>
  );
}
