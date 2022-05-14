import {LOGIN_USER, REGISTER_USER} from "../_actions/types";

const initialState = {
        email: "",
        password: ""
};
// eslint-disable-next-line
export default function(prevState={initialState}, action){
    switch(action.type){
        case LOGIN_USER:
            return{
                ...prevState,
                loginSuccess: action.payload
            }
            // eslint-disable-next-line
            break;
        case REGISTER_USER:
            return{
                ...prevState,
                registerSuccess: action.payload
            }
            // eslint-disable-next-line
            break;
        default:
            return prevState;
    }
}