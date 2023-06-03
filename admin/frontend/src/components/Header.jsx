import Logo from "../assets/logo.svg";

const Header = () => {
    return (
        <>
            <div className='py-[40px] px-[60px] w-[100%] absolute'>
                <div className='flex justify-end mr-2'>
                    <img src={Logo} />
                </div>
                <div className='flex flex-col'>
                    <div className='flex gap-[5px] items-center'>
                        <div className='h-[22px] w-[5px] bg-black'></div>
                        <h1 className='font-black text-[75px]'>Заголовок</h1>
                    </div>
                    <h2 className='font-black text-[180px] text-[#F8F8F8] h-[150px] flex items-center'>
                        Заголовок
                    </h2>
                </div>
            </div>
        </>
    );
};

export default Header;
