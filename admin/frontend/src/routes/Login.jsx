/* eslint-disable no-unused-vars */
import { useState } from "react";
import Form from "../components/Form";
import TextInput from "../components/TextInput";

const Login = () => {
    const [username, setUsername] = useState("");
    const [usernameError, setUsernameError] = useState("");

    const [password, setPassword] = useState("");
    const [passwordError, setPasswordError] = useState("");

    return (
        <>
            <Form header='Login' buttonText='Login'>
                <TextInput
                    value={username}
                    valueSetter={setUsername}
                    error={usernameError}
                    placeholder='Username'
                />
                <TextInput
                    value={password}
                    valueSetter={setPassword}
                    error={passwordError}
                    placeholder='Password'
                    type='password'
                />
            </Form>
        </>
    );
};

export default Login;
