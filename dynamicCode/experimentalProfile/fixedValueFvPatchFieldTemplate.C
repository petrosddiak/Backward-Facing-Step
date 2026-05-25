/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | www.openfoam.com
     \\/     M anipulation  |
-------------------------------------------------------------------------------
    Copyright (C) 2019-2021 OpenCFD Ltd.
    Copyright (C) YEAR AUTHOR, AFFILIATION
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "fixedValueFvPatchFieldTemplate.H"
#include "addToRunTimeSelectionTable.H"
#include "fvPatchFieldMapper.H"
#include "volFields.H"
#include "surfaceFields.H"
#include "unitConversion.H"
#include "PatchFunction1.H"

//{{{ begin codeInclude

//}}} end codeInclude


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

// dynamicCode:
// SHA1 = c3f14a7e1e5593e78499646cf003a72e74663f5a
//
// unique function name that can be checked if the correct library version
// has been loaded
extern "C" void experimentalProfile_c3f14a7e1e5593e78499646cf003a72e74663f5a(bool load)
{
    if (load)
    {
        // Code that can be explicitly executed after loading
    }
    else
    {
        // Code that can be explicitly executed before unloading
    }
}

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

makeRemovablePatchTypeField
(
    fvPatchVectorField,
    experimentalProfileFixedValueFvPatchVectorField
);

} // End namespace Foam


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::
experimentalProfileFixedValueFvPatchVectorField::
experimentalProfileFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(p, iF)
{
    if (false)
    {
        printMessage("Construct experimentalProfile : patch/DimensionedField");
    }
}


Foam::
experimentalProfileFixedValueFvPatchVectorField::
experimentalProfileFixedValueFvPatchVectorField
(
    const experimentalProfileFixedValueFvPatchVectorField& rhs,
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const fvPatchFieldMapper& mapper
)
:
    parent_bctype(rhs, p, iF, mapper)
{
    if (false)
    {
        printMessage("Construct experimentalProfile : patch/DimensionedField/mapper");
    }
}


Foam::
experimentalProfileFixedValueFvPatchVectorField::
experimentalProfileFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const dictionary& dict
)
:
    parent_bctype(p, iF, dict)
{
    if (false)
    {
        printMessage("Construct experimentalProfile : patch/dictionary");
    }
}


Foam::
experimentalProfileFixedValueFvPatchVectorField::
experimentalProfileFixedValueFvPatchVectorField
(
    const experimentalProfileFixedValueFvPatchVectorField& rhs
)
:
    parent_bctype(rhs),
    dictionaryContent(rhs)
{
    if (false)
    {
        printMessage("Copy construct experimentalProfile");
    }
}


Foam::
experimentalProfileFixedValueFvPatchVectorField::
experimentalProfileFixedValueFvPatchVectorField
(
    const experimentalProfileFixedValueFvPatchVectorField& rhs,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(rhs, iF)
{
    if (false)
    {
        printMessage("Construct experimentalProfile : copy/DimensionedField");
    }
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

Foam::
experimentalProfileFixedValueFvPatchVectorField::
~experimentalProfileFixedValueFvPatchVectorField()
{
    if (false)
    {
        printMessage("Destroy experimentalProfile");
    }
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

void
Foam::
experimentalProfileFixedValueFvPatchVectorField::updateCoeffs()
{
    if (this->updated())
    {
        return;
    }

    if (false)
    {
        printMessage("updateCoeffs experimentalProfile");
    }

//{{{ begin code
    #line 32 "/home/petros/cfd_projects/step_duct/0/U/boundaryField/inlet"
const scalar Uref = 44.2;
        const scalar H = 0.0127;

        // Driver and Seegmiller alpha=0 profile at X/H=-4.
        // The table uses absolute Y/H, with the upstream lower wall at Y/H=1.
        const label nData = 19;
        const scalar yByHData[nData] =
        {
            1.00,
            1.10, 1.15, 1.20, 1.30, 1.40, 1.50, 1.70, 2.00,
            2.40, 2.80, 3.20, 3.60, 4.00, 5.00, 6.00, 7.50, 8.20,
            9.00
        };
        const scalar uByUrefData[nData] =
        {
            0.000,
            0.657, 0.696, 0.719, 0.760, 0.790, 0.818, 0.870, 0.926,
            0.982, 1.003, 1.003, 1.000, 1.001, 1.001, 1.000, 1.001, 0.943,
            0.000
        };

        const vectorField& Cf = patch().Cf();
        vectorField& field = *this;

        forAll(Cf, i)
        {
            const scalar yByH = Cf[i].y()/H;
            scalar uByUref = 0;

            if (yByH <= yByHData[0])
            {
                uByUref = uByUrefData[0];
            }
            else if (yByH >= yByHData[nData - 1])
            {
                uByUref = uByUrefData[nData - 1];
            }
            else
            {
                for (label j = 1; j < nData; ++j)
                {
                    if (yByH <= yByHData[j])
                    {
                        const scalar t =
                            (yByH - yByHData[j - 1])/(yByHData[j] - yByHData[j - 1]);
                        uByUref =
                            uByUrefData[j - 1] + t*(uByUrefData[j] - uByUrefData[j - 1]);
                        break;
                    }
                }
            }

            field[i] = vector(Uref*uByUref, 0, 0);
        }
//}}} end code

    this->parent_bctype::updateCoeffs();
}


// ************************************************************************* //

