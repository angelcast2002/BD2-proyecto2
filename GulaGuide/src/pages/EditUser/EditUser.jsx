import React, { useState } from "react"
import style from "./EditUser.module.css"
import { useStoreon } from "storeon/react"
import ComponentInput from "../../components/Input/Input"

const EditUser = () => {

    const [pfpPreview, setPfpPreview] = useState("https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png")
    const { user } = useStoreon("user")


    const [name, setName] = useState(user.name)
    const [email, setEmail] = useState(user.email)
    const [lastname, setLastname] = useState(user.lastname)
    const [budget, setBudget] = useState(user.budget)
    const [pfp, setPfp] = useState(user.pfp)

    const handleInputsValues = (e) => {
        switch (e.target.name) {
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
            default:
                break
        }
    }


    return (
        <div className={style.editUserContainer}>
            <div className={style.mainContainer}>
                <div className={style.imgContainer}>
                    <img src={pfpPreview} alt="profile picture" />
                </div>
                <div className={style.dataContainer}>
                    <div className={style.dataGroup1Container}>
                        <div className={style.nameContainer}>
                            <span>Nombre</span>
                            <ComponentInput
                                name={name}
                                type={"text"}
                                placeholder={name}
                                onChange={handleInputsValues}
                            />
                        </div>
                        <div className={style.lastnameContainer}>
                            <span>Apellido</span>
                            <ComponentInput
                                name={lastname}
                                type={"text"}
                                placeholder={lastname}
                                onChange={handleInputsValues}
                            />
                        </div>
                        <div className={style.budgetContainer}>
                            <span>Presupuesto</span>
                            <ComponentInput
                                name={budget}
                                type={"text"}
                                placeholder={budget}
                                onChange={handleInputsValues}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default EditUser
