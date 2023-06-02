import Form from "../components/Form";
import TextInput from "../components/TextInput";

const Login = () => {
    return (
        <>
            <Form header="Login" buttonText="Login">
                <TextInput placeholder="Username" />
                <TextInput placeholder="Password" inputType="password" />
            </Form>
        </>
    );
};

export default Login;
