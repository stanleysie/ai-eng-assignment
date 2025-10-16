export type Recipe = {
  id: string;
  name: string;
  data: RecipeData;
};

export type RecipeData = {
  author: string;
  categories: string[];
  description: string;
  featured_tweaks: {
    has_modification: boolean;
    is_featured: boolean;
    rating: number;
    text: string;
  }[];
  ingredients: string[];
  instructions: string[];
  nutrition: {
    "@type": string;
    calories: string;
    carbohydrateContent: string;
    cholesterolContent: string;
    fatContent: string;
    fiberContent: string;
    proteinContent: string;
    saturatedFatContent: string;
    sodiumContent: string;
    sugarContent: string;
    unsaturatedFatContent: string;
  };
  rating: {
    count: string;
    value: string;
  };
  recipe_id: string;
  reviews: {
    has_modification?: boolean;
    rating: number;
    text: string;
  }[];
  scraped_at: string;
  servings: string;
  title: string;
  totaltime: string;
  url: string;
};

export type EnhancedRecipe = {
  cook_time: string | null;
  created_at: string;
  description: string;
  enhancement_summary: {
    change_types: string[];
    expected_impact: string;
    total_changes: number;
  };
  ingredients: string[];
  instructions: string[];
  modifications_applied: {
    changes_made: {
      from_text: string;
      operation: string;
      to_text: string;
      type: string;
    }[];
    modification_type: string;
    reasoning: string;
    source_review: {
      rating: number;
      reviewer: string | null;
      text: string;
    };
  }[];
  original_recipe_id: string;
  pipeline_version: string;
  prep_time: string | null;
  recipe_id: string;
  servings: string;
  title: string;
  total_time: string | null;
};
