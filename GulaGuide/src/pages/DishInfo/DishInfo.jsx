import React from "react";
import { useState } from "react";
import { useEffect } from "react";
import style from "./DishInfo.module.css";
import useApi from "../../Hooks/useApi";



const DishInfo = (name_dish) => {

  name_dish = "Pollo Cocido"

  const api = useApi()
  const [dish_info, setDishInfo] = useState(null)

  const gettingDishInfo = async () => {
    let response
    response = await api.handleRequest(
      "GET",
      "get/dish?dish_id=" + name_dish
    )

    const data = await response
    setDishInfo(data[0])
  }

  useEffect(() => {
    gettingDishInfo()
  }, [])

  console.log("dish_info", dish_info)

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

      </div>
      <div className={style.ingredientsContainer} >
        <div className={style.ingredientsText}>
          <h1>Ingredientes</h1>

        </div>
      </div>
    </div>
  );
};

export default DishInfo;