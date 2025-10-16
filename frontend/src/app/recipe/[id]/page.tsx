"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { EnhancedRecipe, Recipe } from "../../../../types/types";
import { useParams } from "next/navigation";

export default function RecipePage() {
  const { id } = useParams();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [isEnhancing, setIsEnhancing] = useState(false);
  const [modificationReferences, setModificationReferences] = useState<
    Record<string, string>
  >({});

  useEffect(() => {
    const fetchRecipe = async () => {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_APP_URL ?? ""}/api/recipe/${id}`
      );
      if (!res.ok) throw new Error("Failed to fetch recipe");
      const data = await res.json();
      setRecipe(data);
    };
    fetchRecipe();
  }, [id]);

  const enhanceRecipe = async () => {
    setIsEnhancing(true);
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_APP_URL ?? ""}/api/recipe/${id}/enhance`
    );
    if (!res.ok) throw new Error("Failed to enhance recipe");
    const data: EnhancedRecipe = await res.json();
    const updatedRecipe = { ...recipe } as Recipe;
    if (updatedRecipe?.data) {
      if (data.instructions) {
        updatedRecipe.data.instructions = data.instructions;
      }
      if (data.ingredients) {
        updatedRecipe.data.ingredients = data.ingredients;
      }
    }
    setRecipe(updatedRecipe);

    const modifications = data.modifications_applied;
    if (!modifications) {
      setIsEnhancing(false);
      return;
    }
    const modificationReferences: Record<string, string> = {};
    for (const modification of modifications) {
      const changes = modification.changes_made;
      for (const change of changes) {
        if (change.type === "instruction") {
          updatedRecipe.data.ingredients = data.ingredients;
        }
        for (const modification of modifications) {
          const changes = modification.changes_made;
          for (const change of changes) {
            modificationReferences[change.to_text] =
              modification.source_review.text;
          }
        }
      }
    }
    setModificationReferences(modificationReferences);
    setIsEnhancing(false);
  };

  return (
    <main className="mx-auto max-w-3xl p-6 space-y-6">
      <Link href="/" className="text-sm text-gray-500">
        ← Back
      </Link>
      {/* Header section: name, description, author, categories */}
      <section className="space-y-3">
        <h1 className="text-3xl font-semibold">{recipe?.name ?? "Recipe"}</h1>
        {recipe?.data?.description ? (
          <p className="text-gray-700 leading-relaxed">
            {recipe.data.description}
          </p>
        ) : null}
        <div className="flex flex-wrap items-center gap-2 text-sm text-gray-600">
          {Array.isArray(recipe?.data?.categories) &&
          recipe.data.categories.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {recipe.data.categories.map((cat: string, idx: number) => (
                <span
                  key={`${cat}-${idx}`}
                  className="px-2 py-0.5 rounded-full bg-gray-100 text-gray-700"
                >
                  {cat}
                </span>
              ))}
            </div>
          ) : null}
        </div>
      </section>

      <button
        className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
        onClick={enhanceRecipe}
        disabled={isEnhancing}
      >
        {isEnhancing ? "Enhancing..." : "Enhance"}
      </button>

      {/* Ingredients section */}
      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Ingredients</h2>
        {Array.isArray(recipe?.data?.ingredients) &&
        recipe.data.ingredients.length > 0 ? (
          <div className="flex flex-wrap gap-3">
            {recipe.data.ingredients.map((item: string, idx: number) => {
              const highlight = modificationReferences[item];
              return (
                <div
                  key={`ing-${idx}`}
                  className={`rounded border border-gray-200 px-3 py-2 text-gray-800 shadow-sm relative ${
                    highlight ? "bg-yellow-200 cursor-help" : "bg-white"
                  }`}
                >
                  <span>{item}</span>
                  {highlight && (
                    <span
                      className="opacity-0 group-hover:opacity-100 absolute left-1/2 -translate-x-1/2 top-full mt-2 z-10 w-max max-w-xs bg-yellow-100 text-gray-900 text-xs px-3 py-2 rounded shadow tooltip transition-opacity duration-200 pointer-events-none"
                      style={{ whiteSpace: "pre-line" }}
                    >
                      {highlight}
                    </span>
                  )}
                  {/* Add group if using tailwind for hover */}
                  {/* We'll wrap this in a span with group class to use group-hover */}
                  <style jsx>{`
                    .relative:hover .tooltip,
                    .group:hover .tooltip {
                      opacity: 1 !important;
                      pointer-events: auto;
                    }
                  `}</style>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="text-sm text-gray-500">No ingredients available.</p>
        )}
      </section>

      {/* Instructions section */}
      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Instructions</h2>
        {Array.isArray(recipe?.data?.instructions) &&
        recipe.data.instructions.length > 0 ? (
          <ol className="list-decimal list-inside space-y-2">
            {recipe.data.instructions.map((item: string, idx: number) => {
              const highlight = modificationReferences[item];
              return (
                <li
                  key={`inst-${idx}`}
                  className={`rounded border border-gray-200 px-3 py-2 text-gray-800 shadow-sm relative ${
                    highlight ? "bg-yellow-200 cursor-help" : "bg-white"
                  }`}
                >
                  <span>{item}</span>
                  {highlight && (
                    <span
                      className="opacity-0 group-hover:opacity-100 absolute left-1/2 -translate-x-1/2 top-full mt-2 z-10 w-max max-w-xs bg-yellow-100 text-gray-900 text-xs px-3 py-2 rounded shadow tooltip transition-opacity duration-200 pointer-events-none"
                      style={{ whiteSpace: "pre-line" }}
                    >
                      {highlight}
                    </span>
                  )}
                  {/* Add group if using tailwind for hover */}
                  {/* We'll wrap this in a span with group class to use group-hover */}
                  <style jsx>{`
                    .relative:hover .tooltip,
                    .group:hover .tooltip {
                      opacity: 1 !important;
                      pointer-events: auto;
                    }
                  `}</style>
                </li>
              );
            })}
          </ol>
        ) : (
          <p className="text-sm text-gray-500">No instructions available.</p>
        )}
      </section>

      {/* Reviews section */}
      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Reviews</h2>
        {Array.isArray(recipe?.data?.reviews) &&
        recipe.data.reviews.length > 0 ? (
          <div className="flex flex-wrap gap-4">
            {recipe.data.reviews.map(
              (
                review: {
                  rating: number;
                  text: string;
                  has_modification?: boolean;
                },
                idx: number
              ) => {
                const rounded = Math.max(
                  0,
                  Math.min(5, Math.round(review.rating))
                );
                const stars = "★".repeat(rounded) + "☆".repeat(5 - rounded);
                return (
                  <div
                    key={`rev-${idx}`}
                    className="w-full sm:w-[calc(50%-0.5rem)] rounded border border-gray-200 bg-white p-3 shadow-sm"
                  >
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <span className="text-yellow-500">{stars}</span>
                      <span className="text-xs text-gray-400">
                        ({review.rating.toFixed(1)})
                      </span>
                    </div>
                    <p className="mt-2 text-gray-800 whitespace-pre-line">
                      {review.text}
                    </p>
                  </div>
                );
              }
            )}
          </div>
        ) : (
          <p className="text-sm text-gray-500">No reviews yet.</p>
        )}
      </section>
    </main>
  );
}
