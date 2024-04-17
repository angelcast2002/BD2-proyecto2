import React from "react";
import { useState } from "react";
import { useEffect } from "react";
import style from "./DinerOnDish.module.css";

import { useStoreon } from "storeon/react";
import useApi from "../../Hooks/useApi";

import Header from "../../components/Header/Header";
import Popup from "../../components/Popup/Popup";
import Button from "../../components/Button/Button";
import { navigate } from "../../store";

const DinerOnDish = ({ id }) => {
  const api = useApi();
  const { user } = useStoreon("user");
  const dish_id = id;

  const [dishInfo, setDishInfo] = useState(null);

  const [error, setError] = useState("");
  const [warning, setWarning] = useState(false);
  const [typeError, setTypeError] = useState("");

  const gettingDishInfo = async () => {
    let response_dish_info;
    response_dish_info = await api.handleRequest(
      "GET",
      "get/dish?dish_id=" + dish_id
    );
    const data = await response_dish_info; // Recibidos
    console.log("data dishes: ->", data)
    console.log("user id:", user.id_user)
    console.log("dish id:", dish_id)
    setDishInfo(data[0]);
  };

  useEffect(() => {
    gettingDishInfo();
  }, []);

  const handleClickAddFavs = async () => {
    const response = await api.handleRequest(
      "POST",
      "dish/opinion",
      {
        dish_id: dishInfo.name,
        diner_id: user.id_user,
        favorite: true,
        likes: true,
        comment: "string"
      }
    )

    const data = await response;
    if (data.status === 200) {
      setError("Añadido a favoritos")
      setTypeError(3)
      setWarning(true)
      setTimeout(() => {
        navigate("/recommendations")
      }, 5000)
    } else {
      setError("Error al añadir a favoritos")
      setTypeError(1)
      setWarning(true)
    }

  }

  return (
    <div className={style.mainContainer}>
      <Header />
      <Popup
        message={error}
        status={warning}
        style={typeError}
        close={() => setWarning(false)}
      />
      <div className={style.Container}>
        <h1>{dishInfo?.name}</h1>
        <div className={style.textContainer}>
          <p>{dishInfo?.description}</p>
          <p>{dishInfo?.has_alcohol ? 'Tiene alcohol' : 'No tiene alcohol'}</p>
          <p>Precio promedio: {"Q." + dishInfo?.avg_price + ".00"}</p>
          <p>{dishInfo?.is_vegan ? 'Es vegano' : 'No es vegano'}</p>
        </div>
        <div className={style.buttonContainer}>
          <Button
            label="Añadir a favoritos"
            backgroundColor="#FFD700"
            onClick={handleClickAddFavs}
          />
        </div>
      </div>
    </div>
  );
}

export default DinerOnDish