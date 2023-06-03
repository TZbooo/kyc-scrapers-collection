/* eslint-disable no-unused-vars */
import { useState } from "react";
import Form from "../components/Form";
import TextInput from "../components/TextInput";

const Register = () => {
    const [username, setUsername] = useState("");
    const [usernameError, setUsernameError] = useState("");

    const [email, setEmail] = useState("");
    const [emailError, setEmailError] = useState("");

    const [password, setPassword] = useState("");
    const [passwordError, setPasswordError] = useState("");

    const [confirmedPassword, setConfirmedPassword] = useState("");
    const [confirmedPasswordError, setConfirmedPasswordError] = useState("");

    return (
        <>
            <Form header='Register' buttonText='Register'>
                <TextInput
                    value={username}
                    valueSetter={setUsername}
                    error={usernameError}
                    placeholder='Username'
                />
                <TextInput
                    value={email}
                    valueSetter={setEmail}
                    error={emailError}
                    placeholder='Email'
                    type='email'
                />
                <TextInput
                    value={password}
                    valueSetter={setPassword}
                    error={passwordError}
                    placeholder='Password'
                    type='password'
                />
                <TextInput
                    value={confirmedPassword}
                    valueSetter={setConfirmedPassword}
                    error={confirmedPasswordError}
                    placeholder='Confirm password'
                    type='password'
                />
            </Form>
        </>
    );
};

export default Register;
