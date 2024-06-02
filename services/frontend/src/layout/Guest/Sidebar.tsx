import { Home, User, Settings } from 'lucide-react';

import {
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
} from '@/components/ui/sheet';

import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
    CommandSeparator,
} from '@/components/ui/command';
import { Link } from '@tanstack/react-router';

const Sidebar = () => {
    return (
        <Sheet>
            <SheetTrigger>
                <div className="flex flex-col gap-1 w-8 hover:cursor-pointer">
                    <span className="border-2 border-white rounded-lg h-1 w-full"></span>
                    <span className="border-2 border-white rounded-lg h-1 w-full"></span>
                    <span className="border-2 border-white rounded-lg h-1 w-full"></span>
                </div>
            </SheetTrigger>
            <SheetContent side={'left'}>
                <SheetHeader>
                    <SheetTitle>Skripsi App</SheetTitle>
                    <SheetDescription>
                        <Command>
                            <CommandInput placeholder="Type here to search ..." />
                            <CommandList>
                                <CommandEmpty>No data</CommandEmpty>
                                <CommandGroup heading="Menu">
                                    <CommandItem>
                                        <Link
                                            to="/"
                                            className="w-full h-full px-4 py-2.5 flex items-center rounded-sm"
                                        >
                                            <Home className="mr-2 h-4 w-4" />
                                            <span>Home</span>
                                        </Link>
                                    </CommandItem>
                                    <CommandItem>
                                        <Link
                                            to="/settings"
                                            className="w-full h-full px-4 py-2.5 flex items-center rounded-sm"
                                        >
                                            <Settings className="mr-2 h-4 w-4" />
                                            <span>Settings</span>
                                        </Link>
                                    </CommandItem>
                                    <CommandItem>
                                        <Link
                                            to="/user"
                                            className="w-full h-full px-4 py-2.5 flex items-center rounded-sm"
                                        >
                                            <User className="mr-2 h-4 w-4" />
                                            <span className="">User</span>
                                        </Link>
                                    </CommandItem>
                                </CommandGroup>
                                <CommandSeparator />
                            </CommandList>
                        </Command>
                    </SheetDescription>
                </SheetHeader>
            </SheetContent>
        </Sheet>
    );
};

export default Sidebar;
