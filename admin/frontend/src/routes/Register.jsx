import { useState } from "react";
import Form from "../components/Form";
import TextInput from "../components/TextInput";

const Register = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmedPassword, setConfirmedPassword] = useState("");

    return (
        <>
            <Form header='Register' buttonText='Register'>
                <TextInput
                    value={username}
                    valueSetter={setUsername}
                    placeholder='Username'
                />
                <TextInput
                    value={email}
                    valueSetter={setEmail}
                    placeholder='Email'
                    type='email'
                />
                <TextInput
                    value={password}
                    valueSetter={setPassword}
                    placeholder='Password'
                    type='password'
                />
                <TextInput
                    value={confirmedPassword}
                    valueSetter={setConfirmedPassword}
                    placeholder='Confirm password'
                    type='password'
                />
            </Form>
        </>
    );
};

export default Register;
