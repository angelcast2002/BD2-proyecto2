import React from "react";
import { useState } from "react";
import { useEffect } from "react";
import style from "./DishInfo.module.css";
import useApi from "../../Hooks/useApi";


const DishInfo = (dish_id) => {

  dish_id = "Pollo Cocido"

  const api = useApi()
  const [dish_info, setDishInfo] = useState(null)
  const [ingredients, setIngredients] = useState(null)

  const gettingDishInfo = async () => {
    let response
    response = await api.handleRequest(
      "GET",
      "get/dish?dish_id=" + dish_id
    )

    const data = await response
    setDishInfo(data[0])
  }

  const gettingIngredients = async () => {
    let response
    response = await api.handleRequest(
      "GET",
      "dish/ingredients?dish_id=" + dish_id
    )

    const data = await response
    setIngredients(data)
  }

  useEffect(() => {
    gettingDishInfo()
    gettingIngredients()
  }, [])

  console.log("dish_info", dish_info)
  console.log("ingredients", ingredients)




  /**
   * has_alcohol
   * is_vegan
   * name
   * description
   * avg_price
   */

  return (
    <div className={style.mainContainer}>
      <div className={style.dishContainer}>
        {dish_info && (
          <div className={style.dishContainerText}>
            <h1>{dish_info.name}</h1>
            <p>
              <strong>{"Descripción: "}</strong> {" "}
              {dish_info.description}
            </p>
            <p>
              <strong>{"Precio promedio: "}</strong> {" "}
              {"Q." + dish_info.avg_price + ".00"}
            </p>
            <p>
              <strong>{"Vegano: "}</strong> {" "}
              {dish_info.is_vegan ? "Sí" : "No"}
            </p>
            <p>
              <strong>{"Contiene alcohol: "}</strong> {" "}
              {dish_info.has_alcohol ? "Sí" : "No"}
            </p>
          </div>
        )}
      </div>style.
      <div className={style.ingredientsContainer}>
        <h1>Ingredientes</h1>
        <div className={style.ingredientsList}>
          {ingredients && ingredients.map((ingredient, index) => {
            return (
              <p>
                {ingredient}
              </p>
            )
          })}
        </div>
      </div>
    </div>
  );
};

export default DishInfo;