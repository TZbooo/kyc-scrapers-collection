import PropTypes from "prop-types";

const ScraperList = ({ name }) => {
    return (
        <>
            <div className="pt-[255px] px-[60px]">
                <div className="flex flex-col gap-2">
                    <h3 className="font-black text-[#828282] text-[45px]">{name}</h3>
                    <div className="flex flex-col gap-[15px]">
                        <div className="h-[116px] w-[100%] border-[#ABABAB] border-[1px] px-[38px] flex justify-between items-center font-semibold font-roboto text-[1.3vw] leading-[28.13px]">
                            <div className="h-[56px] w-[10vw] flex justify-center">телеграм каналы</div>
                            <div className="h-[56px] w-[10vw] flex justify-center">всего взаимодействий</div>
                            <div className="h-[56px] w-[10vw] flex justify-center">за месяц взаимодействий</div>
                            <div className="h-[56px] w-[10vw] flex justify-center">за сегодня взаимодествий</div>
                            <div className="h-[56px] w-[10vw] flex justify-center">информационный источник</div>
                            <div className="h-[56px] w-[10vw] flex justify-center">запуск</div>
                        </div>
                        <div className="h-[184px] w-[100%] border-[#ABABAB] border-[1px] px-[38px] flex justify-between items-center font-normal font-roboto text-[1.1vw] leading-[21.09px]">
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

ScraperList.propTypes = {
    name: PropTypes.string.isRequired,
};

export default ScraperList;
