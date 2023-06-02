import Form from "../components/Form";

const Login = () => {
    return (
        <>
            <Form>
                <h1 className="font-semibold font-roboto text-[2.5em] text-[#1D1D1D]">Login</h1>
                <div className="flex flex-col gap-5">
                    <input className='bg-[#F0F0F0] border-[#C9C9C9] border-[1px] h-[3.5em] w-[705px] rounded-[8px] px-5 font-roboto text-[#1D1D1D]' placeholder="Username" />
                    <input className='bg-[#F0F0F0] border-[#C9C9C9] border-[1px] h-[3.5em] w-[705px] rounded-[8px] px-5 font-roboto text-[#1D1D1D]' placeholder="Password" />
                </div>
                <button className="bg-[#212121] h-[2.9em] w-[174px] text-white text-[1.3em] font-black">Save</button>
            </Form>
        </>
    );
};

export default Login;
