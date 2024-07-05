library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.numeric_std.all;

entity bram_multiplier is
    Port ( 
        clk : in  STD_LOGIC;
        Addr_bram   : out std_logic_vector(15 downto 0);
        EN_bram     : out STD_LOGIC := '0';
        dout_bram   : in  std_logic_vector(31 downto 0);
        RST_bram    : out STD_LOGIC := '1';
        din_bram    : out std_logic_vector(31 downto 0);
        WEB_bram    : out std_logic_vector(3 downto 0);
        Done        : out STD_LOGIC := '0';
        Start       : in  STD_LOGIC
    );
end bram_multiplier;

architecture Behavioral of bram_multiplier is
    constant MATRIX_SIZE : integer := 28;
    constant KERNEL_SIZE : integer := 3;

    signal adr_s  : std_logic_vector(15 downto 0) := (others => '0');
    signal RData1     : std_logic_vector(31 downto 0) := (others => '0');
    signal RData2     : std_logic_vector(31 downto 0) := (others => '0');
    signal WEB_S : std_logic_vector(3 downto 0) := (others => '0');
    signal product : std_logic_vector(31 downto 0) := (others => '0');
    signal Is_Run : STD_LOGIC := '0';
    signal cnt : integer := 0;

    type matrix_28x28 is array (0 to MATRIX_SIZE-1, 0 to MATRIX_SIZE-1) of std_logic_vector(31 downto 0);
    type matrix_3x3 is array (0 to KERNEL_SIZE-1, 0 to KERNEL_SIZE-1) of std_logic_vector(31 downto 0);

    signal input_matrix : matrix_28x28 := (others => (others => (others => '0')));
    signal kernel_matrix : matrix_3x3 := (others => (others => (others => '0')));
    signal result_matrix : matrix_28x28 := (others => (others => (others => '0')));

    signal current_row : integer := 0;
    signal current_col : integer := 0;
    signal kernel_row : integer := 0;
    signal kernel_col : integer := 0;
begin

    Addr_bram <= adr_s;
    RST_bram <= '0';
    EN_bram <= '1';
    WEB_bram <= WEB_S;

    process(clk)
    begin
        if rising_edge(clk) then
            if (Start='1') and (Is_Run = '0') then
                Is_Run <= '1';
                Done <= '0';
                cnt <= 0;
                WEB_S <= "0000";
                adr_s <= (others => '0');
                current_row <= 0;
                current_col <= 0;
                kernel_row <= 0;
                kernel_col <= 0;
            elsif (Is_Run = '1') then
                if cnt < (MATRIX_SIZE * MATRIX_SIZE) then
                    input_matrix(current_row, current_col) <= dout_bram;
                    adr_s <= std_logic_vector(to_unsigned(cnt + 1, 16));
                    cnt <= cnt + 1;
                    current_col <= (current_col + 1) mod MATRIX_SIZE;
                    if current_col = 0 then
                        current_row <= current_row + 1;
                    end if;
                elsif cnt < (MATRIX_SIZE * MATRIX_SIZE + KERNEL_SIZE * KERNEL_SIZE) then
                    kernel_matrix(kernel_row, kernel_col) <= dout_bram;
                    adr_s <= std_logic_vector(to_unsigned(cnt + 1, 16));
                    cnt <= cnt + 1;
                    kernel_col <= (kernel_col + 1) mod KERNEL_SIZE;
                    if kernel_col = 0 then
                        kernel_row <= kernel_row + 1;
                    end if;
                else
                    -- Perform convolution
                    for i in 0 to MATRIX_SIZE-KERNEL_SIZE loop
                        for j in 0 to MATRIX_SIZE-KERNEL_SIZE loop
                            product <= (others => '0');
                            for ki in 0 to KERNEL_SIZE-1 loop
                                for kj in 0 to KERNEL_SIZE-1 loop
                                    product <= std_logic_vector(
                                        resize(
                                            unsigned(product) + unsigned(input_matrix(i+ki, j+kj)) * unsigned(kernel_matrix(ki, kj)), 32
                                        )
                                    );
                                end loop;
                            end loop;
                            result_matrix(i, j) <= product;
                        end loop;
                    end loop;

                    -- Write result back to BRAM
                    if cnt < (MATRIX_SIZE * MATRIX_SIZE + KERNEL_SIZE * KERNEL_SIZE + MATRIX_SIZE * MATRIX_SIZE) then
                        adr_s <= std_logic_vector(to_unsigned(cnt + 1, 16));
                        din_bram <= result_matrix(current_row, current_col);
                        WEB_S <= "1111";
                        cnt <= cnt + 1;
                        current_col <= (current_col + 1) mod MATRIX_SIZE;
                        if current_col = 0 then
                            current_row <= current_row + 1;
                        end if;
                    else
                        Done <= '1';
                        if Start='0' then
                            Is_Run <= '0';
                        end if;
                    end if;
                end if;
            end if;
        end if;
    end process;

end Behavioral;
