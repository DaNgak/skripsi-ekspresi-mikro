import Sidebar from './Sidebar';

const Header = () => {
    return (
        <header className="flex-none py-4 px-10 bg-primary flex justify-between items-center">
            <Sidebar />
            <h1 className="font-semibold text-base tracking-wide text-white">
                Skripsi App
            </h1>
        </header>
    );
};

export default Header;
