import React, {useState} from 'react';
import {useDispatch} from "react-redux";
import {registerUser} from "../_actions/user_action";
import styled from 'styled-components';

const Div = styled.div`
    display: 'flex';
    justify-content: 'center';
    align-items: 'center';
    width: '100%';
    height: '100vh';
    flex-direction: column;
`;
const H2 = styled.h2`
    text-align: center;
`;
const Form = styled.form`
    display:flex;
    flex-direction:column;
`;

const Input = styled.input`
    width: 312px;
    height: 48px;
    font-size: 15px;
    line-height: 1.47;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 13px 12px;
    box-sizing: inherit;
    margin-bottom: 12px;
    padding-block: inherit;
`;

const Button = styled.button`
    margin-top: 12px;
    width: 338px;
    height: 48px;
    font-size: 15px;
`;

const RegisterPage = (props) => {
    const dispatch = useDispatch();

    const [Email, setEmail] = useState("");
    const [Name, setName] = useState("");
    const [Password, setPassword] = useState("");
    const [ConfirmPassword, setConfirmPassword] = useState("");

    const onEmailHandler = (e) => {
        setEmail(e.currentTarget.value);
    }
    const onNameHandler =(e) => {
        setName(e.currentTarget.value);
    }
    const onPasswordHandler = (e) => {
        setPassword(e.currentTarget.value);
    }
    const onConfirmPasswordHandler = (e) => {
        setConfirmPassword(e.currentTarget.value);
    }
    const onSubmitHandler = (e) => {
        e.preventDefault();

        if(Password !== ConfirmPassword){
            return alert("비밀번호와 비밀번호 확인은 같아야 합니다.");
        }

        let body = {
            email: Email,
            name: Name,
            password: Password,
            confirmPassword: ConfirmPassword
        };

        dispatch(registerUser(body))
            .then(response => {
                if(response.payload.registerSuccess){
                    props.history.push('/login');
                }else{
                    alert("Failed to sign up");
                }
            })
    }

    return (
        <Div>
            <H2>SLIRI</H2>
            <Form onSubmit={onSubmitHandler}>
                <label>이메일</label>
                <Input placeholder="example@email.com" type="email" value={Email} onChange={onEmailHandler}/>
                <label>이름</label>
                <Input placeholder="홍길동" type="text" value={Name} onChange={onNameHandler}/>
                <label>비밀번호</label>
                <Input placeholder="******" type="password" value={Password} onChange={onPasswordHandler}/>
                <label>비밀번호 확인</label>
                <Input placeholder="******" type="password" value={ConfirmPassword} onChange={onConfirmPasswordHandler}/>
                <Button>
                    Register
                </Button>
            </Form>

        </Div>
    );
};

export default RegisterPage;