import React from "react";
import style from "./IngredientsList.module.css";

const IngredientsList = ({ ingredients }) => {
  return (
    <div className={style.mainContainer}>
      <h1>Ingredientes</h1>
      <ul>
        {ingredients.map((ingredient) => (
          <li>{ingredient}</li>
        ))}
      </ul>
    </div>
  );
}

export default IngredientsList;