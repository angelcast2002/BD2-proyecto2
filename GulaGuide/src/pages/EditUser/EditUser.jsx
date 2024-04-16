import React, { useState } from "react"
import style from "./EditUser.module.css"
import { useStoreon } from "storeon/react"
import ComponentInput from "../../components/Input/Input"
import { Checkbox } from "@mui/material"




const EditUser = () => {

    const [pfpPreview, setPfpPreview] = useState("https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png")
    const { user } = useStoreon("user")


    const [url, setUrl] = useState("")

    const [name, setName] = useState(user.name)
    const [email, setEmail] = useState(user.email)
    const [lastname, setLastname] = useState(user.lastname)
    const [budget, setBudget] = useState(user.budget)
    const [hasCar, setHasCar] = useState(user.hasCar)
    const [pfp, setPfp] = useState(user.pfp)

    const [minPrice, setMinPrice] = useState(user.minPrice)
    const [maxPrice, setMaxPrice] = useState(user.maxPrice)
    const [minSchedule, setMinSchedule] = useState(user.minSchedule)
    const [maxSchedule, setMaxSchedule] = useState(user.maxSchedule)
    const [petFriendly, setPetFriendly] = useState(user.petFriendly)
    const [sellsAlcohol, setSellsAlcohol] = useState(user.sellsAlcohol)

    const handleInputsValues = (e) => {
        switch (e.target.name) {
            case "url":
                setPfpPreview(e.target.value)
                break
            case "name":
                setName(e.target.value)
                break
            case "email":
                setEmail(e.target.value)
                break
            case "password":
                setPassword(e.target.value)
                break
            case "pfp":
                setPfp(e.target.value)
                break
            case "lastname":
                setLastname(e.target.value)
                break
            case "budget":
                setBudget(e.target.value)
                break
            case "hasCar":
                setHasCar(e.target.checked)
                break
            case "minPrice":
                setMinPrice(e.target.value)
                break
            case "maxPrice":
                setMaxPrice(e.target.value)
                break
            case "minSchedule":
                setMinSchedule(e.target.value)
                break
            case "maxSchedule":
                setMaxSchedule(e.target.value)
                break
            case "petFriendly":
                setPetFriendly(e.target.checked)
                break
            case "sellsAlcohol":
                setSellsAlcohol(e.target.checked)
                break
        }
    }

    console.log(name, email, lastname, budget, hasCar, pfp)
    console.log(user)
    // falta ruta para tener la información del usuario. 

    return (
        <div className={style.editUserContainer}>
            <div className={style.mainContainer}>
                <div className={style.imgContainer}>
                    <img src={pfpPreview} alt="profile picture" />
                </div>
                <div className={style.dataContainer}>
                    {user.role === "Diner" && (
                        <div className={style.dataGroup1Container}>
                            <div className={style.urlContainer}>
                                <span>URL de la foto de perfil</span>
                                <ComponentInput
                                    name={url}
                                    type={"text"}
                                    value={url}
                                    onChange={handleInputsValues}
                                />
                            </div>
                            <div className={style.nameContainer}>
                                <span>Nombre</span>
                                <ComponentInput
                                    name={name}
                                    type={"text"}
                                    value={name}
                                    onChange={handleInputsValues}
                                />
                            </div>
                            <div className={style.lastnameContainer}>
                                <span>Apellido</span>
                                <ComponentInput
                                    name={lastname}
                                    type={"text"}
                                    value={lastname}
                                    onChange={handleInputsValues}
                                />
                            </div>
                            <div className={style.budgetContainer}>
                                <span>Presupuesto</span>
                                <ComponentInput
                                    name={budget}
                                    type={"text"}
                                    value={budget}
                                    onChange={handleInputsValues}
                                />
                            </div>
                            <div className={style.hascarContainer}>
                                <span>¿Tienes auto?</span>
                                <Checkbox
                                    name="Vehiculo"
                                    onChange={handleInputsValues}
                                />
                            </div>
                        </div>
                    )}
                    {user.role === "Restaurant" && (
                        <div className={style.dataGroup2Container}>
                            <div className={style.nameContainer}>
                                <span>Nombre del Restaurante</span>
                                <ComponentInput
                                    name={name}
                                    type={"text"}
                                    value={name}
                                    onChange={handleInputsValues}
                                />
                            </div>
                            <div className={style.priceRangeContainer}>
                                <span>Rango de Precios</span>
                                <div className={style.priceRangeContainerInt}>
                                    <ComponentInput
                                        name={minPrice}
                                        type={"text"}
                                        placeholder={"Mínimo"}
                                        value={minPrice}
                                        onChange={handleInputsValues}
                                    />
                                    <ComponentInput
                                        name={maxPrice}
                                        type={"text"}
                                        placeholder={"Máximo"}
                                        value={maxPrice}
                                        onChange={handleInputsValues}
                                    />
                                </div>
                            </div>
                            <div className={style.priceRangeContainer}>
                                <span>Horario</span>
                                <div className={style.priceRangeContainerInt}>
                                    <ComponentInput
                                        name={minSchedule}
                                        type={"text"}
                                        placeholder={"Mínimo"}
                                        value={minSchedule}
                                        onChange={handleInputsValues}
                                    />
                                    <ComponentInput
                                        name={maxSchedule}
                                        type={"text"}
                                        placeholder={"Máximo"}
                                        value={maxSchedule}
                                        onChange={handleInputsValues}
                                    />
                                </div>
                            </div>
                            <div className={style.checkboxContainer}>
                                <div className={style.priceRangeContainerInt}>
                                    <span>¿Acepta mascotas?</span>
                                    <Checkbox
                                        name="Acepta Mascotas"
                                        onChange={handleInputsValues}
                                    />
                                </div>
                                <div className={style.priceRangeContainerInt}>
                                    <span>¿Vende Alcohol?</span>
                                    <Checkbox
                                        name="Vende Alcohol"
                                        onChange={handleInputsValues}
                                    />
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default EditUser
