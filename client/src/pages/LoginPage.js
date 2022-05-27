import React, {useState} from 'react';
import {useDispatch} from "react-redux";
import {loginUser} from "../_actions/user_action";
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

const LoginPage = (props) => {
    const dispatch = useDispatch();

    const [Email, setEmail] = useState("");
    const [Password, setPassword] = useState("");

    const onEmailHandler = (e) => {
        setEmail(e.currentTarget.value);
    }
    const onPasswordHandler = (e) => {
        setPassword(e.currentTarget.value);
    }
    const onSubmitHandler = (e) => {
        e.preventDefault();
        props.history.push('/');

    }

    return (
        <Div>
            <H2>SLIRI</H2>
            <Form onSubmit={onSubmitHandler}>
                <Input placeholder="example@email.com" type="email" value={Email} required onChange={onEmailHandler}/>
                <Input placeholder="******" type="password" value={Password} required onChange={onPasswordHandler}/>
                <Button>
                    Login
                </Button>
            </Form>
        </Div>
    );
};

export default LoginPage;