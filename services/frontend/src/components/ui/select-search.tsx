import { Check, ChevronsUpDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
} from '@/components/ui/command';
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from '@/components/ui/popover';
import { useState, useEffect } from 'react';

interface IProps {
    options: { label: string; value: string }[];
    placeholder?: string;
    onChange: (value: string) => void;
}

export function Select({ options, placeholder, onChange }: IProps) {
    const [open, setOpen] = useState(false);
    const [value, setValue] = useState('');

    useEffect(() => {
        console.log('Select options:', JSON.stringify(options, null, 2));
        options.forEach((element) => {
            console.log(element);
        });
    }, [options]);

    const handleOnSelect = (currentValue: string) => {
        const newValue = currentValue === value ? '' : currentValue;
        setValue(newValue);
        onChange(newValue);
        setOpen(false);
    };

    return (
        <Popover
            open={open}
            onOpenChange={setOpen}
        >
            <PopoverTrigger asChild>
                <Button
                    variant="outline"
                    role="combobox"
                    aria-expanded={open}
                    className="w-[200px] justify-between"
                >
                    {/* {value
                        ? options.find((option) => option.value === value)
                              ?.label
                        : placeholder || 'Select option...'} */}
                    <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[200px] p-0">
                <Command>
                    <CommandInput
                        placeholder={placeholder || 'Select option...'}
                    />
                    <CommandEmpty>No data</CommandEmpty>
                    <CommandGroup>
                        {options.map((option) => (
                            <CommandItem
                                key={option.value}
                                value={option.value}
                                onSelect={() => handleOnSelect(option.value)}
                            >
                                <Check
                                    className={cn(
                                        'mr-2 h-4 w-4',
                                        value === option.value
                                            ? 'opacity-100'
                                            : 'opacity-0'
                                    )}
                                />
                                {option.label}
                            </CommandItem>
                        ))}
                    </CommandGroup>
                </Command>
            </PopoverContent>
        </Popover>
    );
}
