import Form from "../components/Form";
import TextInput from "../components/TextInput";

const Register = () => {
    return (
        <>
            <Form header="Register" buttonText="Register">
                <TextInput placeholder="Username" />
                <TextInput placeholder="Email" inputType="email" />
                <TextInput placeholder="Password" inputType="password" />
                <TextInput placeholder="Confirm password" inputType="password" />
            </Form>
        </>
    );
};

export default Register;
