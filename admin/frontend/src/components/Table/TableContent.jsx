import TableItem from "./TableItem";

const TableContent = () => {
    const tableItems = [
        {
            id: "4dc47c26-391c-488a-ab9d-e3246ee29c2a",
            name: "Название тг канала",
            total: 1234,
            totalPerMonth: 1234,
            totalPerDay: 1234,
            origin: "https://t.me/example",
            isRunning: false,
        },
        {
            id: "87d9e4d2-1064-4c67-b991-259bbd55c9b8",
            name: "Название тг канала",
            total: 1234,
            totalPerMonth: 1234,
            totalPerDay: 1234,
            origin: "https://t.me/example",
            isRunning: true,
        },
    ];

    return (
        <>
            {tableItems.map((tableItem) => (
                <TableItem
                    key={tableItem.id}
                    id={tableItem.id}
                    name={tableItem.name}
                    total={tableItem.total}
                    totalPerMonth={tableItem.totalPerMonth}
                    totalPerDay={tableItem.totalPerDay}
                    origin={tableItem.origin}
                    isRunning={tableItem.isRunning}
                />
            ))}
        </>
    );
};

export default TableContent;
