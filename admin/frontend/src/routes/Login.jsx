import { useState } from "react";
import Form from "../components/Form";
import TextInput from "../components/TextInput";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    return (
        <>
            <Form header='Login' buttonText='Login'>
                <TextInput
                    value={username}
                    valueSetter={setUsername}
                    placeholder='Username'
                />
                <TextInput
                    value={password}
                    valueSetter={setPassword}
                    placeholder='Password'
                    inputType='password'
                />
            </Form>
        </>
    );
};

export default Login;
