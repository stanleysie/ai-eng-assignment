import { Recipe } from "../../types/types";
import Link from "next/link";

async function fetchRecipes() {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_APP_URL ?? ""}/api/recipes`,
    {
      cache: "no-store",
    }
  );
  if (!res.ok) throw new Error("Failed to load");
  return res.json() as Promise<Recipe[]>;
}

export default async function Home() {
  const recipes = await fetchRecipes();
  return (
    <main className="mx-auto max-w-3xl p-6 space-y-6">
      <h1 className="text-2xl font-semibold mb-4">Recipes</h1>
      <ul className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {recipes.map((r) => (
          <li
            key={r.id}
            className="w-full rounded border border-gray-200 bg-white p-4 shadow-sm flex items-center justify-between"
          >
            <div>
              <div className="font-medium text-gray-900">{r.name}</div>
              <div className="text-xs text-gray-400">ID: {r.id}</div>
            </div>
            <Link
              href={`/recipe/${r.id}`}
              className="px-3 py-1.5 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Open
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
